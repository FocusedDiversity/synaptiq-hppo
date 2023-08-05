import os

from slack_bolt.adapter.socket_mode.websockets import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp

from chatbae.llm import chat_mod

SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)


@app.event("app_home_opened")
async def handle_app_home_opened_events(body, logger):
    logger.info(body)


@app.event("message")
async def event_im_message(event, say):
    prompt = event["text"]
    chat_mod.prefill(input=prompt)
    response = "Houston, we have a problem"
    while not chat_mod.stopped():
        chat_mod.decode()
        response = chat_mod.get_message()
    await say(response)


@app.command("/hello-bolt-python")
async def command(ack, body, respond):
    await ack()
    await respond(f"Hi <@{body['user_id']}>!")


async def start_async_handler():
    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()

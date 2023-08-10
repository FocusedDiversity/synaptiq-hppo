import os

from mlc_chat import ChatModule
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp

from chatbae.response_generator import ResponseGenerator

SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")


async def init_slack_bot(chat_mod: ChatModule):
    app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

    @app.event("app_home_opened")
    async def handle_app_home_opened_events(body, logger):
        logger.info(body)

    @app.event("message")
    async def event_im_message(event, say):
        prompt = event["text"]
        chat_mod.prefill(input=prompt)
        o = ResponseGenerator()
        while not chat_mod.stopped():
            chat_mod.decode()
            response = o.update(chat_mod.get_message())
            if response:
                await say(response)
        await o.update(chat_mod.get_message(), final=True)

    @app.command("/hello-bolt-python")
    async def command(ack, body, respond):
        await ack()
        await respond(f"Hi <@{body['user_id']}>!")

    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()

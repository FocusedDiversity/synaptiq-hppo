import os

from mlc_chat import ChatModule
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp

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
        offset = 0
        while not chat_mod.stopped():
            chat_mod.decode()
            response = chat_mod.get_message()
            if "\n" in response[offset:]:
                new_offset = len(response)
                await say(response[offset:new_offset])
                offset = new_offset
        await say(response[offset:])

    @app.command("/hello-bolt-python")
    async def command(ack, body, respond):
        await ack()
        await respond(f"Hi <@{body['user_id']}>!")

    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()

import os
import asyncio

from databricks.sdk import WorkspaceClient
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp

# from functools import lru_cache
# from chatbot.response_generator import ResponseGenerator

w = WorkspaceClient()
dbutils = w.dbutils

SLACK_APP_TOKEN = dbutils.secrets.get("hippo", "SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = dbutils.secrets.get("hippo", "SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = dbutils.secrets.get("hippo", "SLACK_SIGNING_SECRET")


# async def init_slack_bot(chat_mod_factory):
async def init_slack_bot():
    app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

    # @lru_cache(maxsize=5)
    # def user_chat_mod(user):
    #     return chat_mod_factory(user)

    @app.event("app_home_opened")
    async def handle_app_home_opened_events(body, logger):
        logger.info(body)

    @app.event("message")
    async def event_im_message(event, say):
        user = event["user"]
        say(
            f"Hi there {user}! I'm not yet configured to do anything but say 'Hi there!'"
        )
        # chat_mod = user_chat_mod(event["user"])
        # prompt = event["text"]
        # if "##reset" in prompt:
        #     chat_mod.reset_chat()
        #     return

        # chat_mod._prefill(input=prompt)
        # o = ResponseGenerator()
        # while not chat_mod._stopped():
        #     chat_mod._decode()
        #     response = o.update(chat_mod._get_message())
        #     if response:
        #         await say(response)
        # final = o.update(chat_mod._get_message(), final=True)
        # if final:
        #     await say(final)

    @app.command("/hello-bolt-python")
    async def command(ack, body, respond):
        await ack()
        await respond(f"Hi <@{body['user_id']}>!")

    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(init_slack_bot())

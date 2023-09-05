# Databricks notebook source
import nest_asyncio
nest_asyncio.apply()

# COMMAND ----------

import os
import asyncio
from slack_bolt.adapter.socket_mode.aiohttp import AsyncSocketModeHandler
from slack_bolt.app.async_app import AsyncApp

# COMMAND ----------

SLACK_APP_TOKEN = dbutils.secrets.get("hippo", "SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = dbutils.secrets.get("hippo", "SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = dbutils.secrets.get("hippo", "SLACK_SIGNING_SECRET")

# COMMAND ----------

async def init_slack_bot():
    app = AsyncApp(token=SLACK_BOT_TOKEN, signing_secret=SLACK_SIGNING_SECRET)

    @app.event("app_home_opened")
    async def handle_app_home_opened_events(body, logger):
        logger.info(body)

    @app.event("message")
    async def event_im_message(event, say):
        user = event["user"]
        await say(
            f"Hi there {user}! I'm not yet configured to do anything but say 'Hi there!'"
        )

    @app.command("/hello-bolt-python")
    async def command(ack, body, respond):
        await ack()
        await respond(f"Hi <@{body['user_id']}>!")

    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()

# COMMAND ----------

asyncio.run(init_slack_bot())

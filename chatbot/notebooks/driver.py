# Databricks notebook source
import asyncio

import nest_asyncio

from chatbot.bot import init_slack_bot

# COMMAND ----------

nest_asyncio.apply()

# COMMAND ----------

SLACK_APP_TOKEN = dbutils.secrets.get("hippo", "SLACK_APP_TOKEN")
SLACK_BOT_TOKEN = dbutils.secrets.get("hippo", "SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = dbutils.secrets.get("hippo", "SLACK_SIGNING_SECRET")

# COMMAND ----------

asyncio.run(init_slack_bot(SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, SLACK_APP_TOKEN))

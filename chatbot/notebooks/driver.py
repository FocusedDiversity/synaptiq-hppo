# Databricks notebook source
!ls ..

# COMMAND ----------

!pip install -e ../chatbae

# COMMAND ----------

dbutils.secrets.get("hippo", "SLACK_BOT_TOKEN")

# COMMAND ----------



# Databricks notebook source
#Mounting Azure Data Lake
configs_gen2_dev = {"fs.azure.account.auth.type": "OAuth",
                          "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
                          "fs.azure.account.oauth2.client.id": "ecd1a442-9cc0-4d82-bce2-9e9b558de268",
                          "fs.azure.account.oauth2.client.secret": "nrB8Q~vhuRrIhej1hbpg-_Ygf668AskYWUFqIdvm",
                          "fs.azure.account.oauth2.client.endpoint": "https://login.microsoftonline.com/212495af-5ba4-4e31-8511-40118051eaaf/oauth2/token"}

# COMMAND ----------

dbutils.fs.unmount("/mnt/dev/")

# COMMAND ----------

dbutils.fs.mount(
  source = "abfss://test-dir@rxdevtrainingst.dfs.core.windows.net/",  
  mount_point = "/mnt/dev/",
  extra_configs = configs_gen2_dev)

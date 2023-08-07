-- Databricks notebook source
DESCRIBE HISTORY delta.`dbfs:/Azure_Training/org_file`

-- COMMAND ----------

SELECT * FROM delta.`dbfs:/Azure_Training/org_file` VERSION AS OF 1;

-- COMMAND ----------

select * from delta.`dbfs:/Azure_Training/org_file`

-- COMMAND ----------

create database dev_db

-- COMMAND ----------

CREATE TABLE IF NOT EXISTS dev_db.org_data_dump
USING delta
location 'dbfs:/Azure_Training/org_data_dump'
AS
select * from delta.`dbfs:/Azure_Training/org_file`

-- COMMAND ----------



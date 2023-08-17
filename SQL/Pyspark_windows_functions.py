# Databricks notebook source
# File location and type
file_location = "/FileStore/tables/sales_data_sample.csv"
file_type = "csv"

# CSV options
infer_schema = "True"
first_row_is_header = "True"
delimiter = ","

# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

display(df)

# COMMAND ----------

# Create a view or table

temp_table_name = "sales_data_sample_csv"

df.createOrReplaceTempView(temp_table_name)

# COMMAND ----------

from pyspark.sql.window import *
#from pyspark.sql.functions import row_number
windowspec=Window.orderBy("ORDERDATE")
df.withColumn("seq_no",row_number().over(windowspec))


# COMMAND ----------



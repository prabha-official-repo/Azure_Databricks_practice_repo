# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ## Overview
# MAGIC
# MAGIC This notebook will show you how to create and query a table or DataFrame that you uploaded to DBFS. [DBFS](https://docs.databricks.com/user-guide/dbfs-databricks-file-system.html) is a Databricks File System that allows you to store data for querying inside of Databricks. This notebook assumes that you have a file already inside of DBFS that you would like to read from.
# MAGIC
# MAGIC This notebook is written in **Python** so the default cell type is Python. However, you can use different languages by using the `%LANGUAGE` syntax. Python, Scala, SQL, and R are all supported.

# COMMAND ----------

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

# MAGIC %sql
# MAGIC
# MAGIC /* Query the created temp table in a SQL cell */
# MAGIC
# MAGIC select count(distinct ORDERNUMBER) from `sales_data_sample_csv`

# COMMAND ----------

# DBTITLE 1,Row_number and rank,dense_rank
# MAGIC %sql
# MAGIC -- select *,row_number() over (order by orderdate desc) as seq_number
# MAGIC --  from sales_data_sample_csv
# MAGIC
# MAGIC -- select * from (
# MAGIC -- select *,row_number() over (partition by ORDERNUMBER order by orderdate desc ) as seq_number
# MAGIC --  from sales_data_sample_csv
# MAGIC -- )
# MAGIC --  where seq_number=1
# MAGIC
# MAGIC
# MAGIC --  select * from (
# MAGIC -- select *,rank() over (partition by ORDERNUMBER order by SALES desc ) as seq_number
# MAGIC --  from sales_data_sample_csv
# MAGIC -- )
# MAGIC
# MAGIC  select * from (
# MAGIC select *,dense_rank() over (partition by ORDERNUMBER order by PRICEEACH desc ) as seq_number
# MAGIC  from sales_data_sample_csv
# MAGIC )
# MAGIC where PRODUCTLINE='Vintage Cars'
# MAGIC

# COMMAND ----------

# DBTITLE 1,Ntile
# MAGIC %sql
# MAGIC
# MAGIC select *,ntile(4) over (order by SALES desc ) as quartile
# MAGIC  from sales_data_sample_csv

# COMMAND ----------

# DBTITLE 1,Lead and Lag
# MAGIC %sql
# MAGIC -- select *,
# MAGIC -- lag(sales) over(partition by ORDERNUMBER order by ORDERDATE) as prev_amount,
# MAGIC -- lead(sales) over(partition by ORDERNUMBER order by ORDERDATE) as next_amount
# MAGIC -- from sales_data_sample_csv
# MAGIC
# MAGIC
# MAGIC select ORDERNUMBER,sales,PRODUCTLINE,ORDERDATE,
# MAGIC lag(sales) over(order by ORDERDATE desc) as prev_amount,
# MAGIC lead(sales) over(order by ORDERDATE desc) as next_amount
# MAGIC from sales_data_sample_csv

# COMMAND ----------

# DBTITLE 1,SUM
# MAGIC %sql
# MAGIC select ORDERNUMBER,sales,PRODUCTLINE,ORDERDATE,
# MAGIC sum(sales) over(partition by ORDERNUMBER order by ORDERDATE desc) as max_amount,
# MAGIC avg(sales) over(partition by ORDERNUMBER order by ORDERDATE desc) as avg_amount
# MAGIC from sales_data_sample_csv

# COMMAND ----------

# DBTITLE 1,first and last value
# MAGIC %sql
# MAGIC select  ORDERNUMBER,sales,PRODUCTLINE,ORDERDATE,
# MAGIC first_value(sales) over(partition by ORDERNUMBER order by ORDERDATE desc) as first_sale,
# MAGIC last_value(sales) over(partition by ORDERNUMBER order by ORDERDATE desc) as last_sale
# MAGIC from sales_data_sample_csv

# COMMAND ----------



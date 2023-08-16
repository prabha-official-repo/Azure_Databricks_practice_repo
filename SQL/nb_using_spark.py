# Databricks notebook source

dbutils.widgets.text("sourcefilepath","")
dbutils.widgets.text("targetfilepath","")

source_path=dbutils.widgets.get("sourcefilepath")
target_path=dbutils.widgets.get("targetfilepath")
print(source_path)
print(target_path)

# COMMAND ----------

from pyspark.sql.functions import col
def remove_bda_chars_from_columns(df):
    return  df.select([col(x).alias(x.replace(" ", "_").replace("/", "").replace("%", "pct").replace("(", "").replace(")", "")) for x in df.columns])


# COMMAND ----------

# DBTITLE 1,Reading from Azure Data lake using PySpark

#/mnt/dev/organizations-10000_1.csv
org_df = spark.read.option("delimiter",",").option("header",True).csv(f"/mnt/dev/organizations-10000_1.csv")
org_df.withColumnRenamed("Organization Id","Organization_Id").withColumnRenamed("Number of employees","Number_of_employees")
display(org_df)
final_df=remove_bda_chars_from_columns(org_df)




# COMMAND ----------

# DBTITLE 1,Writing into Azure Data lake using PySpark
#final_df.write.mode("overwrite").format("delta").option("header",True).save("dbfs:/Azure_Training/org_file")

# COMMAND ----------


#dbfs:/Azure_Training/org_file
final_df.write.mode("overwrite").format("delta").option("header",True).save(f"dbfs:/Azure_Training/org_file")

# COMMAND ----------



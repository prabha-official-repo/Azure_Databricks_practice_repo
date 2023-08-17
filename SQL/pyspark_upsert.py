# Databricks notebook source
from pyspark.sql.functions import current_timestamp

# COMMAND ----------

source_data = [
    (1, "Alice", "123 Main St", "2023-01-01"),
    (2, "Bob", "456 Elm St", "2023-01-01"),
    (3, "Alicia", "789 Oak Ave", "2023-08-14")]
source_df=spark.createDataFrame(source_data,["id","name","address","effective_date"])
source_df.write.format("delta").save("dbfs:/Azure_Training/scd_type_2_file")

# COMMAND ----------

target_df = spark.read.format("delta").load("dbfs:/Azure_Training/scd_type_2_file")
target_df = target_df.withColumn("end_date", current_timestamp())

# COMMAND ----------

inc_date = [
    (4, "paul", "124 Main St", "2023-01-10"),
    (2, "Bob", "500 Elm St", "2023-02-01"),
    (3, "Alicia", "800 Oak Ave", "2023-09-14")]

inc_data_df=spark.createDataFrame(inc_date,["id","name","address","effective_date"])

# COMMAND ----------

inc_data_df.createOrReplaceTempView("source")
target_df.createOrReplaceTempView("target")

# COMMAND ----------

display(spark.sql("""
    SELECT
        COALESCE(t.id, s.id) AS id,
        COALESCE(s.name, t.name) AS name,
        COALESCE(s.address, t.address) AS address,
        t.start_date,
        s.effective_date AS end_date
    FROM target t
    FULL OUTER JOIN source s ON t.id = s.id
    WHERE t.end_date IS NULL OR t.end_date > s.effective_date
"""))

# COMMAND ----------

# MAGIC %fs ls 'dbfs:/Azure_Training/scd_type_2_file'

# COMMAND ----------

# MAGIC %sql
# MAGIC optimize delta.`dbfs:/Azure_Training/scd_type_2_file`
# MAGIC

# COMMAND ----------

# DBTITLE 1,Using Merge scd type2

#name","address","effective_date"]
inc_data_df.alias('source') \
  .merge(
    target_df.alias('target'),
    'surce.id = target.id'
  ) \
  .whenMatchedUpdate(set =
    {
      "id": "target.id",
      "name": "target.name",
      "address": "target.address",
      "effective_date": "target.effective_date"
    }
  ) \
  .whenNotMatchedInsert(values =
    {
      "id": "target.id",
      "name": "target.name",
      "address": "target.address",
      "effective_date": "target.effective_date"
    }
  ) \
  .execute()

# Databricks notebook source

from pyspark.sql.functions import when,lit
from pyspark.sql import functions as F
# File location and type
file_location = "/FileStore/tables/employee_data.csv"
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
df=df.withColumn("salary",
                 when(F.col("EMPLOYEE_ID").eqNullSafe("121"),lit(9000)).otherwise(F.col("salary"))) \
                     .withColumn("FIRST_NAME",when(F.col("EMPLOYEE_ID").eqNullSafe("121"),\
                         lit("Ashok")).otherwise(F.col("FIRST_NAME")))


display(df)

# COMMAND ----------

# MAGIC %fs ls '/FileStore/tables/'

# COMMAND ----------

# Create a view or table

temp_table_name = "employee_data"

df.createOrReplaceTempView(temp_table_name)

# COMMAND ----------

from pyspark.sql.window import *
from pyspark.sql import functions as F
#from pyspark.sql.functions import row_number
windowspec=Window.partitionBy("EMPLOYEE_ID").orderBy(F.col("HIRE_DATE").desc())
df.withColumn("seq_no",F.row_number().over(windowspec))
display(df)


# COMMAND ----------

# MAGIC %sql
# MAGIC  select * from (
# MAGIC select *,--case when salary=lag(salary) over (order by salary) then 1 else 2 end as sal_comp, 
# MAGIC dense_rank() over (partition by DEPARTMENT_ID order by salary desc) as max_sal
# MAGIC  from employee_data
# MAGIC  )
# MAGIC  where max_sal=1 order by salary desc ,FIRST_NAME asc
# MAGIC

# COMMAND ----------

windowspec1=Window.partitionBy("DEPARTMENT_ID").orderBy(F.col("salary").desc())
df=df.withColumn("max_sal",F.dense_rank().over(windowspec1)).where("max_sal=1")
display(df)

# COMMAND ----------

window_spec2 = Window.orderBy("HIRE_DATE")
df=df.withColumn("prev_amount", F.lag("salary").over(window_spec2))\
        .withColumn("next_amount", F.lead("salary").over(window_spec2))
display(df)

# COMMAND ----------

window_spec = Window.orderBy("HIRE_DATE").rowsBetween(Window.unboundedPreceding,Window.currentRow)
df=df.withColumn("running_total", F.sum("salary").over(window_spec))\
        .withColumn("moving_avg", F.avg("salary").over(window_spec))
display(df)

# COMMAND ----------

window_spec1 = Window.orderBy("HIRE_DATE").rowsBetween(Window.unboundedPreceding, Window.currentRow)
df=df.withColumn("first_sale", F.first("salary").over(window_spec1))\
        .withColumn("last_sale", F.last("salary").over(window_spec1))
display(df)

# COMMAND ----------

# DBTITLE 1,SCD TYPE2
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Sample data for demonstration
source_data = [
    (1, "John Doe", 101),
    (2, "Jane Smith", 102),
    (3, "Michael Johnson", 101),
    (4, "Alice Brown", 103)
]

# COMMAND ----------

dimension_data = [
    (1, "John Doe", 101, "2023-08-01", "9999-12-31"),
    (2, "Jane Smith", 102, "2023-08-01", "9999-12-31"),
    (3, "Mike Johnson", 101, "2023-08-01", "2023-08-15"),
]

# Create DataFrames
source_df = spark.createDataFrame(source_data, ["employee_id", "employee_name", "department_id"])
dimension_df = spark.createDataFrame(dimension_data, ["employee_id", "employee_name", "department_id", "valid_from", "valid_to"])


# COMMAND ----------

# Perform SCD Type 2 operation
window_spec = Window.partitionBy("employee_id").orderBy(F.col("valid_from").desc())
latest_record = dimension_df.withColumn("latest", F.row_number().over(window_spec))\
                            .where(F.col("latest") == 1) \
                            .select("employee_id", "valid_from")
display(latest_record)

# COMMAND ----------

display(source_df.join(latest_record,on="employee_id",how="left_outer")\
    .withColumn("valid_from",when(F.col("valid_from").isNull(),lit(F.current_date()))\
        .otherwise(F.col("valid_from")))\
            .withColumn("valid_to",when(F.col("valid_from").isNull(),lit("9999-12-31"))\
                .otherwise(F.date_sub(F.col("valid_from"),1)))\
    .union(dimension_df.select("employee_id", "employee_name", "department_id", "valid_from", "valid_to")).orderBy("employee_id", "valid_from")

        
        
        
        )

# COMMAND ----------



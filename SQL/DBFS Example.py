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
file_location = "/FileStore/tables/department_data.csv"
file_location1 = "/FileStore/tables/employee_data.csv"
file_type = "csv"

# CSV options
infer_schema = "True"
first_row_is_header = "True"
delimiter = ","

# The applied options are for CSV files. For other file types, these will be ignored.
dep = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

emp = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location1)



# COMMAND ----------

# Create a view or table

temp_table_name1 = "dep"

dep.createOrReplaceTempView(temp_table_name1)

temp_table_name2 = "emp"

emp.createOrReplaceTempView(temp_table_name2)

# COMMAND ----------

SELECT
    employee_name,
    department_name,
    salary,
    CASE
        WHEN salary = LAG(salary) OVER (PARTITION BY department_id ORDER BY salary DESC) THEN 'Same as Previous'
        ELSE 'Different'
    END AS salary_comparison
FROM employees e
JOIN departments d ON e.department_id = d.department_id
ORDER BY department_id, salary DESC;








# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC /* Query the created temp table in a SQL cell */
# MAGIC
# MAGIC select *,
# MAGIC case when max_sal=lag(max_sal) over (partition by  department_id order by first_name asc) then first_name end as first_name  from (
# MAGIC select e.first_name,d.DEPARTMENT_NAME,
# MAGIC max(salary) over(partition by e.department_id) as max_sal
# MAGIC from emp e join dep d on e.department_id=d.department_id
# MAGIC )
# MAGIC

# COMMAND ----------

# With this registered as a temp view, it will only be available to this particular notebook. If you'd like other users to be able to query this table, you can also create a table from the DataFrame.
# Once saved, this table will persist across cluster restarts as well as allow various users across different notebooks to query this data.
# To do so, choose your table name and uncomment the bottom line.

permanent_table_name = "department_data_csv"

# df.write.format("parquet").saveAsTable(permanent_table_name)

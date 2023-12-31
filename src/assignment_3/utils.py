from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import StringType, StructType, StructField, IntegerType
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("../../assignment_2.log"),
        logging.StreamHandler(sys.stdout)
    ])


def sparkSession():
    spark = SparkSession.builder.master("local[1]").appName("Assignment_3").getOrCreate()
    logging.info("Created spark session")
    return spark


def create_dataframe(spark):
    data_product = [
        ("banana", 1000, "USA"),
        ("carrots", 1500, "INDIA"),
        ("beans", 1600, "SWEDEN"),
        ("orange", 2000, "UK"),
        ("orange", 2000, "UAE"),
        ("banana", 400, "CHINA"),
        ("carrots", 1200, "CHINA")
    ]
    schema_product = StructType([
        StructField("Product", StringType(), True),
        StructField("Amount", IntegerType(), True),
        StructField("Country", StringType(), True)
    ])
    product_dataframe = spark.createDataFrame(data=data_product, schema=schema_product)
    logging.info("Created  dataframe with the details")
    return product_dataframe


def total_amount_pivot(product_dataframe):
    pivot_df = product_dataframe.groupBy("Product").pivot("Country").sum("Amount")
    logging.info("Got total_amount_pivot ")
    return pivot_df


def unpivot_dataframe(product_dataframe):
    unpivot_Expr = "stack(6,'China',china,'India',india,'Sweden',sweden,'UAE',uae,'UK',uk,'USA',usa) as (Country,Total)"
    unpivot_df = product_dataframe.select("Product", expr(unpivot_Expr)) \
        .where("Total is not null")
    logging.info("Got unpivot_dataframe")
    return unpivot_df

import datetime
from pyspark.sql import SparkSession, DataFrame, Row
from pyspark.sql import functions as F
from logger.logger import Logger
from logger.log_scope import LogScope
from logger.log_levels import LogLevel

def process_specific_words(spark: SparkSession, df: DataFrame, output_dir: str) -> None:
    """
    Process the dataset to count specific words in the 'description' column.

    Args:
        spark (SparkSession): The active Spark session.
        df (DataFrame): The input dataset DataFrame.
        output_dir (str): The directory path where the output parquet file will be saved.
    """
    logger = Logger.get_logger(LogScope.PROCESS_DATA)
    specific_words = ["president", "the", "Asia"]

    df_words = df.select(F.explode(F.split(F.col("description"), "\\W+")).alias("word")).filter(F.col("word") != "")
    counts_df = df_words.filter(F.col("word").isin(specific_words)) \
                         .groupBy("word") \
                         .agg(F.count("*").alias("word_count"))

    words_df = spark.createDataFrame([Row(word=w) for w in specific_words])
    result = words_df.join(counts_df, on="word", how="left").fillna(0, subset=["word_count"])

    today = datetime.datetime.today().strftime("%Y%m%d")
    output_path = f"{output_dir}/word_count_{today}.parquet"
    result.write.mode("overwrite").parquet(output_path)
    logger.log(f"Specific word count saved to {output_path}", LogLevel.INFO)

def process_all_words(spark: SparkSession, df: DataFrame, output_dir: str) -> None:
    """
    Process the dataset to count all unique words in the 'description' column.

    Args:
        spark (SparkSession): The active Spark session.
        df (DataFrame): The input dataset DataFrame.
        output_dir (str): The directory path where the output parquet file will be saved.
    """
    logger = Logger.get_logger(LogScope.PROCESS_DATA_ALL)
    df_words = df.select(F.explode(F.split(F.col("description"), "\\W+")).alias("word")).filter(F.col("word") != "")
    result = df_words.groupBy("word").agg(F.count("*").alias("count"))

    today = datetime.datetime.today().strftime("%Y%m%d")
    output_path = f"{output_dir}/word_count_all_{today}.parquet"
    result.write.mode("overwrite").parquet(output_path)
    logger.log(f"All word counts saved to {output_path}", LogLevel.INFO)

from pyspark.sql import SparkSession, DataFrame
from datasets import load_dataset
from logger.logger import Logger
from logger.log_scope import LogScope
from logger.log_levels import LogLevel

def create_spark_session(app_name: str = "DataProcessing") -> SparkSession:
    """
    Create and return a Spark session.

    Args:
        app_name (str): Name of the Spark application.

    Returns:
        SparkSession: An active Spark session.
    """
    logger = Logger.get_logger(LogScope.SPARK)
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    logger.log(f"Spark session '{app_name}' created.", LogLevel.INFO)
    return spark

def download_dataset(spark: SparkSession, config: dict) -> DataFrame:
    """
    Download the AG News dataset using Hugging Face datasets and load it as a Spark DataFrame.

    Args:
        spark (SparkSession): The active Spark session.
        config (dict): Configuration dictionary containing keys "dataset_name" and "split".

    Returns:
        DataFrame: A Spark DataFrame containing the dataset.
    """
    logger = Logger.get_logger(LogScope.SPARK)
    dataset_name = config.get("dataset_name", "sh0416/ag_news")
    split = config.get("split", "test")
    logger.log(f"Loading dataset '{dataset_name}' with split '{split}' using Hugging Face datasets", LogLevel.INFO)
    dataset = load_dataset(dataset_name, split=split)
    pdf = dataset.to_pandas()
    df = spark.createDataFrame(pdf)
    logger.log(f"Dataset '{dataset_name}' loaded and converted to Spark DataFrame.", LogLevel.INFO)
    return df

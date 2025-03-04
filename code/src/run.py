"""
Main script for processing the AG News dataset.

This script supports two commands:
- process_data: Counts the occurrences of three specific words ("president", "the", "Asia")
  in the "description" column of the AG News dataset.
- process_data_all: Tokenizes the "description" column and counts all unique words.

Usage examples:
    python src/run.py process_data --cfg config/cfg.yaml -dataset news --dirout "ztmp/data/"
    python src/run.py process_data_all --cfg config/cfg.yaml -dataset news --dirout "ztmp/data/"
"""

import argparse
import datetime
import logging
import yaml
from pyspark.sql import SparkSession, DataFrame, Row
from pyspark.sql import functions as F

def load_config(cfg_path: str) -> dict:
    """
    Load configuration from a YAML file.
    
    Args:
        cfg_path (str): Path to the YAML configuration file.
    
    Returns:
        dict: Dictionary with configuration parameters.
    """
    with open(cfg_path, "r") as f:
        config = yaml.safe_load(f)
    return config

def create_spark_session(app_name: str = "DataProcessing") -> SparkSession:
    """
    Create and return a Spark session.
    
    Args:
        app_name (str): Name of the Spark application.
    
    Returns:
        SparkSession: An active Spark session.
    """
    spark = SparkSession.builder.appName(app_name).getOrCreate()
    return spark

def download_dataset(spark: SparkSession, config: dict) -> DataFrame:
    """
    Download the AG News dataset using Hugging Face datasets and load it as a Spark DataFrame.
    
    This function loads the dataset using the Hugging Face 'load_dataset' method.
    It converts the dataset to a Pandas DataFrame and then creates a Spark DataFrame.
    
    Args:
        spark (SparkSession): The active Spark session.
        config (dict): Configuration dictionary containing keys "dataset_name" and "split".
    
    Returns:
        DataFrame: A Spark DataFrame containing the dataset.
    """
    from datasets import load_dataset
    dataset_name = config.get("dataset_name", "sh0416/ag_news")
    split = config.get("split", "test")
    logging.info(f"Loading dataset '{dataset_name}' with split '{split}' using Hugging Face datasets")
    dataset = load_dataset(dataset_name, split=split)
    pdf = dataset.to_pandas()
    df = spark.createDataFrame(pdf)
    return df

def process_specific_words(spark: SparkSession, df: DataFrame, output_dir: str) -> None:
    """
    Process the dataset to count specific words in the 'description' column.
    
    It counts the occurrences of the words "president", "the", and "Asia" (case sensitive)
    and saves the resulting table as a parquet file.
    
    Args:
        spark (SparkSession): The active Spark session.
        df (DataFrame): The input dataset DataFrame.
        output_dir (str): The directory path where the output parquet file will be saved.
    """
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
    logging.info(f"Specific word count saved to {output_path}")

    with open("logs/Data_processed.txt", "w") as log_file:
        log_file.write("Data processing complete for specific words.\n")

def process_all_words(spark: SparkSession, df: DataFrame, output_dir: str) -> None:
    """
    Process the dataset to count all unique words in the 'description' column.
    
    The function tokenizes the text by splitting on any non-word character and computes the frequency
    of each word. The result is saved as a parquet file.
    
    Args:
        spark (SparkSession): The active Spark session.
        df (DataFrame): The input dataset DataFrame.
        output_dir (str): The directory path where the output parquet file will be saved.
    """
    df_words = df.select(F.explode(F.split(F.col("description"), "\\W+")).alias("word")).filter(F.col("word") != "")
    result = df_words.groupBy("word").agg(F.count("*").alias("count"))
    
    today = datetime.datetime.today().strftime("%Y%m%d")
    output_path = f"{output_dir}/word_count_all_{today}.parquet"
    result.write.mode("overwrite").parquet(output_path)
    logging.info(f"All words count saved to {output_path}")

    with open("logs/Data_processed_all.txt", "w") as log_file:
        log_file.write("Data processing complete for all words.\n")

def main():
    parser = argparse.ArgumentParser(description="AI Data Engineer Assignment Application")
    subparsers = parser.add_subparsers(dest="command", help="Sub-command to run")

    parser_process_data = subparsers.add_parser("process_data", help="Process specific words data")
    parser_process_data.add_argument("--cfg", required=True, help="Path to config file")
    parser_process_data.add_argument("-dataset", required=True, help="Dataset type (e.g., news)")
    parser_process_data.add_argument("--dirout", required=True, help="Output directory for parquet file")

    parser_process_data_all = subparsers.add_parser("process_data_all", help="Process all words data")
    parser_process_data_all.add_argument("--cfg", required=True, help="Path to config file")
    parser_process_data_all.add_argument("-dataset", required=True, help="Dataset type (e.g., news)")
    parser_process_data_all.add_argument("--dirout", required=True, help="Output directory for parquet file")

    args = parser.parse_args()

    # Configure logging to write to a file
    log_filename = f"logs_{datetime.datetime.today().strftime('%Y%m%d')}.log"
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s",
                        handlers=[logging.FileHandler(log_filename), logging.StreamHandler()])

    logging.info("Starting the application")
    
    config = load_config(args.cfg)
    logging.info("Configuration loaded.")
    
    spark = create_spark_session("AI_Data_Engineer_Assignment")
    logging.info("Spark session created.")

    if args.dataset.lower() == "news":
        df = download_dataset(spark, config)
        logging.info("Dataset loaded.")
    else:
        logging.error(f"Dataset type '{args.dataset}' is not supported.")
        spark.stop()
        return

    if args.command == "process_data":
        process_specific_words(spark, df, args.dirout)
    elif args.command == "process_data_all":
        process_all_words(spark, df, args.dirout)
    else:
        logging.error("No valid command provided.")
    
    spark.stop()
    logging.info("Application finished")


if __name__ == "__main__":
    main()
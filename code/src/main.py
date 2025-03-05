import argparse
from config.config import load_config
from spark.spark_utils import create_spark_session, download_dataset
from processing.processing import process_specific_words, process_all_words
from logger.logger import Logger
from logger.log_levels import LogLevel
from logger.log_scope import LogScope

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

    app_logger = Logger.get_logger(LogScope.APPLICATION)
    app_logger.log("Starting the application", LogLevel.INFO)

    config = load_config(args.cfg)
    app_logger.log("Configuration loaded.", LogLevel.INFO)

    spark = create_spark_session("AI_Data_Engineer_Assignment")
    app_logger.log("Spark session created.", LogLevel.INFO)

    if args.dataset.lower() == "news":
        df = download_dataset(spark, config)
        app_logger.log("Dataset loaded.", LogLevel.INFO)
    else:
        app_logger.log(f"Dataset type '{args.dataset}' is not supported.", LogLevel.ERROR)
        spark.stop()
        return

    if args.command == "process_data":
        process_logger = Logger.get_logger(LogScope.PROCESS_DATA)
        process_logger.log("Processing specific words data.", LogLevel.INFO)
        process_specific_words(spark, df, args.dirout)
    elif args.command == "process_data_all":
        process_logger = Logger.get_logger(LogScope.PROCESS_DATA_ALL)
        process_logger.log("Processing all words data.", LogLevel.INFO)
        process_all_words(spark, df, args.dirout)
    else:
        app_logger.log("No valid command provided.", LogLevel.ERROR)

    spark.stop()
    app_logger.log("Application finished", LogLevel.INFO)

if __name__ == "__main__":
    main()

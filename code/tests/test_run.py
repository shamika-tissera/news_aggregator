import os
import sys
import shutil
import datetime
import pytest
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from run import load_config, create_spark_session, download_dataset, process_specific_words, process_all_words


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    spark = SparkSession.builder.master("local[2]").appName("TestApp").getOrCreate()
    yield spark
    spark.stop()


@pytest.fixture
def sample_data(spark: SparkSession) -> DataFrame:
    data = [
        ("Today is a test for president and Asia",),
        ("The president said the world is changing",),
        ("Asia is a continent",)
    ]
    return spark.createDataFrame(data, ["description"])


def test_process_specific_words(spark: SparkSession, sample_data: DataFrame, tmp_path):
    output_dir = str(tmp_path)
    process_specific_words(spark, sample_data, output_dir)
    today = datetime.datetime.today().strftime("%Y%m%d")
    expected_file = f"word_count_{today}.parquet"
    files = os.listdir(output_dir)
    assert any(expected_file in f for f in files), "Specific words output not generated."


def test_process_all_words(spark: SparkSession, sample_data: DataFrame, tmp_path):
    output_dir = str(tmp_path)
    process_all_words(spark, sample_data, output_dir)
    today = datetime.datetime.today().strftime("%Y%m%d")
    expected_file = f"word_count_all_{today}.parquet"
    files = os.listdir(output_dir)
    assert any(expected_file in f for f in files), "All words output not generated."
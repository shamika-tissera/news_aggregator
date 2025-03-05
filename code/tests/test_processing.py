import pytest
from pyspark.sql import SparkSession
from pyspark.sql import Row
import os
import datetime
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))
from processing.processing import process_specific_words

@pytest.fixture(scope="module")
def spark():
    return SparkSession.builder.master("local[1]").appName("pytest").getOrCreate()

@pytest.fixture
def sample_df(spark):
    data = [
        Row(description="The president of the United States"),
        Row(description="Asia is the largest continent"),
        Row(description="The president visited Asia"),
        Row(description="The quick brown fox jumps over the lazy dog")
    ]
    return spark.createDataFrame(data)

def test_process_specific_words(spark, sample_df, tmpdir):
    output_dir = tmpdir.mkdir("output")
    process_specific_words(spark, sample_df, str(output_dir))

    today = datetime.datetime.today().strftime("%Y%m%d")
    output_path = os.path.join(str(output_dir), f"word_count_{today}.parquet")

    assert os.path.exists(output_path)

    result_df = spark.read.parquet(output_path)
    result_data = {row['word']: row['word_count'] for row in result_df.collect()}

    assert result_data["president"] == 2
    assert result_data["the"] == 4
    assert result_data["Asia"] == 2

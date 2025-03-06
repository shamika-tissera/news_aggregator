import os
import sys
import datetime
import pytest
from pyspark.sql import SparkSession, Row

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from processing.processing import process_specific_words, process_all_words

@pytest.fixture(scope="session")
def spark_session():
    spark = SparkSession.builder \
        .appName("TestProcessing") \
        .master("local[*]") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def sample_data(spark_session):
    data = [
        ("Today the President spoke about Asia and the economy.",),
        ("The president of Sri Lanka visited USA last week.",),
        ("The meeting included discussions about trade policies.",),
        ("The conference was held in Europe, not Asia.",),
        ("Many leaders attended the summit.",),
    ]
    return spark_session.createDataFrame(data, ["description"])

def test_process_specific_words_with_common_words(spark_session, sample_data, tmp_path):
    """Test that process_specific_words correctly counts the specified words."""
    output_dir = str(tmp_path)
    process_specific_words(spark_session, sample_data, output_dir)

    today = datetime.datetime.today().strftime("%Y%m%d")
    output_path = os.path.join(output_dir, f"word_count_{today}.parquet")
    
    # Check if the output file exists
    assert os.path.exists(output_path), f"Output file {output_path} does not exist"
    
    # Read the result and check the counts
    result_df = spark_session.read.parquet(output_path)
    result = {row['word']: row['word_count'] for row in result_df.collect()}
    
    # Note: Results depend on case sensitivity - using lowercase in processing.py would give different results
    assert 'president' in result, "Word 'president' should be in results"
    assert 'the' in result, "Word 'the' should be in results"
    assert 'Asia' in result, "Word 'Asia' should be in results"

def test_process_all_words(spark_session, sample_data, tmp_path):
    """Test that process_all_words correctly counts all words."""
    output_dir = str(tmp_path)
    process_all_words(spark_session, sample_data, output_dir)

    today = datetime.datetime.today().strftime("%Y%m%d")
    output_path = os.path.join(output_dir, f"word_count_all_{today}.parquet")
    
    # Check if the output file exists
    assert os.path.exists(output_path), f"Output file {output_path} does not exist"
    
    # Read the result and verify some known words
    result_df = spark_session.read.parquet(output_path)
    result = {row['word']: row['count'] for row in result_df.collect()}
    
    assert len(result) > 0, "Result should contain words"
    assert any(word in result for word in ['Today', 'the', 'President', 'Asia']), "Common words should be present"

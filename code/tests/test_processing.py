import unittest
from pyspark.sql import SparkSession
from pyspark.sql import Row
from processing.processing import process_specific_words, process_all_words
import os

class TestProcessing(unittest.TestCase):
    def setUp(self):
        self.spark = SparkSession.builder.master("local").appName("Test").getOrCreate()
        self.df = self.spark.createDataFrame([Row(description="The president of Asia")])
        self.output_dir = "output"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def tearDown(self):
        self.spark.stop()
        for file in os.listdir(self.output_dir):
            os.remove(os.path.join(self.output_dir, file))
        os.rmdir(self.output_dir)

    def test_process_specific_words(self):
        process_specific_words(self.spark, self.df, self.output_dir)
        output_files = os.listdir(self.output_dir)
        self.assertTrue(any("word_count" in file for file in output_files))

    def test_process_all_words(self):
        process_all_words(self.spark, self.df, self.output_dir)
        output_files = os.listdir(self.output_dir)
        self.assertTrue(any("word_count_all" in file for file in output_files))

if __name__ == '__main__':
    unittest.main()

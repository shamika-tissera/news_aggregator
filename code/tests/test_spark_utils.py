import unittest
from spark.spark_utils import create_spark_session, download_dataset

class TestSparkUtils(unittest.TestCase):
    def test_create_spark_session(self):
        spark = create_spark_session("TestApp")
        self.assertIsNotNone(spark)
        spark.stop()

    def test_download_dataset(self):
        spark = create_spark_session("TestApp")
        config = {'dataset_name': 'sh0416/ag_news', 'split': 'test'}
        df = download_dataset(spark, config)
        self.assertIsNotNone(df)
        self.assertGreater(df.count(), 0)
        spark.stop()

if __name__ == '__main__':
    unittest.main()

import unittest
from config.config import load_config
import os

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config_path = 'config/test_config.yaml'
        with open(self.config_path, 'w') as f:
            f.write("dataset_name: 'sh0416/ag_news'\nsplit: 'test'")

    def tearDown(self):
        os.remove(self.config_path)

    def test_load_config(self):
        config = load_config(self.config_path)
        self.assertIsInstance(config, dict)
        self.assertIn('dataset_name', config)
        self.assertIn('split', config)
        self.assertEqual(config['dataset_name'], 'sh0416/ag_news')
        self.assertEqual(config['split'], 'test')

if __name__ == '__main__':
    unittest.main()

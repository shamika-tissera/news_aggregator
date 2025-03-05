import unittest
from unittest.mock import patch
import main
import argparse

class TestMain(unittest.TestCase):
    @patch('argparse.ArgumentParser.parse_args')
    def test_main_process_data(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            command='process_data', cfg='config/config.yaml', dataset='news', dirout='output'
        )
        with patch('main.process_specific_words') as mock_process:
            main.main()
            mock_process.assert_called_once()

    @patch('argparse.ArgumentParser.parse_args')
    def test_main_process_data_all(self, mock_parse_args):
        mock_parse_args.return_value = argparse.Namespace(
            command='process_data_all', cfg='config/config.yaml', dataset='news', dirout='output'
        )
        with patch('main.process_all_words') as mock_process:
            main.main()
            mock_process.assert_called_once()

if __name__ == '__main__':
    unittest.main()

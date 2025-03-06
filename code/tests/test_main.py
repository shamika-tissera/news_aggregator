import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from main import main

@pytest.fixture
def mock_logger():
    with patch('main.Logger') as mock:
        logger_instance = MagicMock()
        mock.get_logger.return_value = logger_instance
        yield mock, logger_instance

@pytest.fixture
def mock_config():
    with patch('main.load_config') as mock:
        mock.return_value = {"dataset_name": "test_dataset", "split": "test"}
        yield mock

@pytest.fixture
def mock_spark():
    with patch('main.create_spark_session') as mock:
        spark_instance = MagicMock()
        mock.return_value = spark_instance
        yield mock, spark_instance

@pytest.fixture
def mock_dataset():
    with patch('main.download_dataset') as mock:
        df = MagicMock()
        mock.return_value = df
        yield mock, df

@pytest.fixture
def mock_process_specific():
    with patch('main.process_specific_words') as mock:
        yield mock

@pytest.fixture
def mock_process_all():
    with patch('main.process_all_words') as mock:
        yield mock

def test_process_data_command(mock_logger, mock_config, mock_spark, mock_dataset, 
                             mock_process_specific, mock_process_all):
    """Test the process_data command execution path"""
    test_args = ['main.py', 'process_data', '--cfg', 'test_config.yaml', 
                '-dataset', 'news', '--dirout', 'test_output']
    
    with patch('sys.argv', test_args):
        main()
        
    # Verify expected function calls
    mock_config.assert_called_once_with('test_config.yaml')
    mock_spark[0].assert_called_once_with('AI_Data_Engineer_Assignment')
    mock_dataset[0].assert_called_once()
    mock_process_specific.assert_called_once_with(mock_spark[1], mock_dataset[1], 'test_output')
    mock_process_all.assert_not_called()
    mock_spark[1].stop.assert_called_once()

def test_process_data_all_command(mock_logger, mock_config, mock_spark, mock_dataset, 
                                 mock_process_specific, mock_process_all):
    """Test the process_data_all command execution path"""
    test_args = ['main.py', 'process_data_all', '--cfg', 'test_config.yaml', 
                '-dataset', 'news', '--dirout', 'test_output']
    
    with patch('sys.argv', test_args):
        main()
        
    # Verify expected function calls
    mock_config.assert_called_once_with('test_config.yaml')
    mock_spark[0].assert_called_once_with('AI_Data_Engineer_Assignment')
    mock_dataset[0].assert_called_once()
    mock_process_all.assert_called_once_with(mock_spark[1], mock_dataset[1], 'test_output')
    mock_process_specific.assert_not_called()
    mock_spark[1].stop.assert_called_once()

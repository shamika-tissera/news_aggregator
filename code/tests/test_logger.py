import logging
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/')))

from logger.logger import Logger
from logger.log_scope import LogScope
from logger.log_levels import LogLevel

import pytest

def test_singleton_pattern():
    logger1 = Logger.get_logger(LogScope.APPLICATION)
    logger2 = Logger.get_logger(LogScope.APPLICATION)
    assert logger1 is logger2

def test_logger_creation():
    logger = Logger.get_logger(LogScope.APPLICATION)
    assert logger is not None
    assert isinstance(logger, Logger)

def test_logger_duplicate_creation():
    Logger.get_logger(LogScope.APPLICATION)
    with pytest.raises(Exception) as excinfo:
        Logger(LogScope.APPLICATION)
    assert str(excinfo.value) == "This logger already exists!"

def test_log_info_level():
    logger = Logger.get_logger(LogScope.APPLICATION)
    logger.log("This is an info message", LogLevel.INFO)
    assert logger.logger.level == logging.INFO

def test_log_warning_level():
    logger = Logger.get_logger(LogScope.APPLICATION)
    logger.log("This is a warning message", LogLevel.WARNING)
    assert logger.logger.level == logging.INFO

def test_log_error_level():
    logger = Logger.get_logger(LogScope.APPLICATION)
    logger.log("This is an error message", LogLevel.ERROR)
    assert logger.logger.level == logging.INFO

def test_log_debug_level():
    logger = Logger.get_logger(LogScope.APPLICATION)
    logger.log("This is a debug message", LogLevel.DEBUG)
    assert logger.logger.level == logging.INFO


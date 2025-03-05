import unittest
from logger.logger import Logger
from logger.log_scope import LogScope
from logger.log_levels import LogLevel
import os

class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger.get_logger(LogScope.APPLICATION)

    def test_get_logger(self):
        self.assertIsNotNone(self.logger)

    def test_log_info(self):
        self.logger.log("Test info message", LogLevel.INFO)
        self.assertTrue(os.path.exists('logs/application.log'))

    def test_log_warning(self):
        self.logger.log("Test warning message", LogLevel.WARNING)
        self.assertTrue(os.path.exists('logs/application.log'))

    def test_log_error(self):
        self.logger.log("Test error message", LogLevel.ERROR)
        self.assertTrue(os.path.exists('logs/application.log'))

    def test_log_debug(self):
        self.logger.log("Test debug message", LogLevel.DEBUG)
        self.assertTrue(os.path.exists('logs/application.log'))

if __name__ == '__main__':
    unittest.main()

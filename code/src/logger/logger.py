import logging
from .log_levels import LogLevel
from .log_scope import LogScope

class Logger:
    """
    A Logger class that provides logging functionality with different scopes.
    This class uses the singleton pattern to ensure only one logger per scope.
    """
    __loggers = {}

    @staticmethod
    def get_logger(scope: LogScope):
        """
        Static access method to get a logger by scope.

        Args:
            scope (LogScope): The scope of the logger.

        Returns:
            Logger: The logger instance for the given scope.
        """
        if scope not in Logger.__loggers:
            Logger.__loggers[scope] = Logger(scope)
        return Logger.__loggers[scope]

    def __init__(self, scope: LogScope):
        """
        Virtually private constructor.

        Args:
            scope (LogScope): The scope of the logger.

        Raises:
            Exception: If a logger for the given scope already exists.
        """
        if scope in Logger.__loggers:
            raise Exception("This logger already exists!")
        else:
            self.logger = logging.getLogger(scope.value)
            self.logger.setLevel(logging.INFO)
            file_handler = logging.FileHandler(f"logs/{scope.value}.log")
            stream_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
            self.logger.addHandler(stream_handler)

    def log(self, message: str, level: LogLevel = LogLevel.INFO):
        """
        Log a message with the given log level.

        Args:
            message (str): The message to log.
            level (LogLevel): The log level (default is LogLevel.INFO).
        """
        if level == LogLevel.INFO:
            self.logger.info(message)
        elif level == LogLevel.WARNING:
            self.logger.warning(message)
        elif level == LogLevel.ERROR:
            self.logger.error(message)
        elif level == LogLevel.DEBUG:
            self.logger.debug(message)
        else:
            self.logger.info(message)

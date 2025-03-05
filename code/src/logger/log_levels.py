from enum import Enum

class LogLevel(Enum):
    """
    Enum for defining different log levels.

    Attributes:
        INFO: Informational messages that highlight the progress of the application.
        WARNING: Potentially harmful situations.
        ERROR: Error events that might still allow the application to continue running.
        DEBUG: Detailed information, typically of interest only when diagnosing problems.
    """
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    DEBUG = "debug"

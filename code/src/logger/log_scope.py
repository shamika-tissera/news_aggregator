from enum import Enum

class LogScope(Enum):
    """
    Enum for defining different log scopes.

    Attributes:
        APPLICATION: Scope for application-wide logs.
        PROCESS_DATA: Scope for logs related to processing specific words data.
        PROCESS_DATA_ALL: Scope for logs related to processing all words data.
        SPARK: Scope for logs related to Spark operations.
        CONFIG: Scope for logs related to configuration operations.
    """
    APPLICATION = "application"
    PROCESS_DATA = "process_data"
    PROCESS_DATA_ALL = "process_data_all"
    SPARK = "spark"
    CONFIG = "config"

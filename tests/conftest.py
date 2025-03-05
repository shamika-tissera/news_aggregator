import sys

class ImportBlocker:
    def __init__(self, modules):
        self.modules = modules

    def __enter__(self):
        for module in self.modules:
            sys.modules[module] = None

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

with ImportBlocker(['log_levels', 'log_scope', 'logger']):
    pass
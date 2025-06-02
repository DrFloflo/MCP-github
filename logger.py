import sys
from datetime import datetime

class SimpleLogger:
    LEVELS = {
        "DEBUG": 10,
        "INFO": 20,
        "WARNING": 30,
        "ERROR": 40,
    }

    def __init__(self, level="INFO"):
        self.level = self.LEVELS.get(level.upper(), 20)

    def _log(self, level_name, message):
        if self.LEVELS[level_name] >= self.level:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] {level_name}: {message}", file=sys.stdout)

    def debug(self, message):
        self._log("DEBUG", message)

    def info(self, message):
        self._log("INFO", message)

    def warning(self, message):
        self._log("WARNING", message)

    def error(self, message):
        self._log("ERROR", message)
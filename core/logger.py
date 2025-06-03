import logging
import sys
import logging.handlers
import queue
from typing import Dict, Any
import json

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', pretty_print=False):
        super().__init__(fmt, datefmt, style)
        self.pretty_print = pretty_print

    def format(self, record: logging.LogRecord) -> str:
        # Create a copy of the record's extra data
        extra_data: Dict[str, Any] = {}
        for key, value in record.__dict__.items():
            if key not in ['args', 'asctime', 'created', 'exc_info', 'exc_text', 
                          'filename', 'funcName', 'id', 'levelname', 'levelno', 
                          'lineno', 'module', 'msecs', 'message', 'msg', 
                          'name', 'pathname', 'process', 'processName', 
                          'relativeCreated', 'stack_info', 'thread', 'threadName']:
                extra_data[key] = value

        # Format the basic log message
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
            **extra_data
        }

        # Handle exceptions
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        if record.stack_info:
            log_entry["stack_info"] = self.formatStack(record.stack_info)

        # Pretty print for console, compact for files
        if self.pretty_print:
            return json.dumps(log_entry, indent=2, ensure_ascii=False)
        return json.dumps(log_entry, ensure_ascii=False)

class StreamHandlerByLevel(logging.Handler):
    def emit(self, record):
        stream = sys.stderr if record.levelno >= logging.ERROR else sys.stdout
        formatter = self.formatter
        try:
            msg = formatter.format(record)
            stream.write(msg + '\n')
            stream.flush()
        except Exception:
            self.handleError(record)

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a log queue
log_queue = queue.Queue(-1)

# Create handlers for output
stream_handler = StreamHandlerByLevel()
stream_handler.setFormatter(CustomFormatter())

# Handlers for the listener
handlers = [stream_handler]

# Set up QueueHandler and add it to the logger
queue_handler = logging.handlers.QueueHandler(log_queue)
logger.addHandler(queue_handler)

# Set up QueueListener with the handlers
listener = logging.handlers.QueueListener(log_queue, *handlers)
listener.start()

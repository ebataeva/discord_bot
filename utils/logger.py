

import logging
import sys
import os
from datetime import datetime

class ColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[94m',     # Blue
        'INFO': '\033[92m',      # Green
        'WARNING': '\033[93m',   # Yellow
        'ERROR': '\033[91m',     # Red
        'CRITICAL': '\033[95m',  # Magenta
    }
    RESET = '\033[0m'

    def format(self, record):
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)

def setup_logger(name="discord_bot", level=logging.INFO, log_to_file=True):
    # Create formatter with function name and timestamp
    formatter = ColorFormatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Optional file handler
        if log_to_file:
            os.makedirs("logs", exist_ok=True)
            filename = datetime.now().strftime("logs/log_%Y%m%d_%H%M%S.log")
            file_handler = logging.FileHandler(filename, encoding='utf-8')
            file_formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | %(name)s | %(funcName)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

    logger.propagate = False
    return logger

logger = setup_logger()
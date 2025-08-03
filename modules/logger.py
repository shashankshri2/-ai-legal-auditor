import logging
import os
import sys

def setup_logger():
    os.makedirs("logs", exist_ok=True)
    logger = logging.getLogger("AuditLogger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # File handler — supports full Unicode (emojis)
        file_handler = logging.FileHandler("logs/audit.log", encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler — ASCII only (avoids emoji error on Windows)
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter("%(asctime)s — %(levelname)s — %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger

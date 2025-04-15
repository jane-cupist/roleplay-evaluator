import logging
import os
from datetime import datetime


def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(message)s")

    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


evaluator_logger = setup_logger(
    "evaluator", f'logs/evaluator_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
)

chat_logger = setup_logger(
    "chat", f'logs/chat_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
)

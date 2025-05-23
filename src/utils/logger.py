import argparse
import logging
import os
from datetime import datetime


def get_model_name(model) -> str:
    if model == "cl":
        return "claude"
    elif model == "ge":
        return "gemini"
    elif model == "ll":
        return "llama"
    elif model == "gp":
        return "gpt"


def get_log_file_name(name: str) -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("--persona-index", type=int)
    parser.add_argument("--companion-index", type=int)
    parser.add_argument("--model", type=str)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--repeat", type=int)
    args = parser.parse_args()

    return f'logs/{name}_{get_model_name(args.model)}_turn{args.limit}_char{args.companion_index}_repeat{args.repeat}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'


def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(message)s")
    log_file = get_log_file_name(name)

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


evaluator_logger = setup_logger("evaluator")
chat_logger = setup_logger("chat")

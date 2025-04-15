import logging
import os
from datetime import datetime


def setup_logger(name: str, log_file: str = None) -> logging.Logger:
    """
    로거를 설정하고 반환합니다.

    Args:
        name: 로거 이름
        log_file: 로그 파일 경로 (None이면 콘솔에만 출력)

    Returns:
        logging.Logger: 설정된 로거 객체
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 로그 포맷 설정
    formatter = logging.Formatter("%(message)s")

    # 파일 핸들러 추가 (log_file이 제공된 경우)
    if log_file:
        # 로그 디렉토리 생성
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# 전역 로거 인스턴스 생성
evaluator_logger = setup_logger(
    "evaluator", f'logs/evaluator_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
)

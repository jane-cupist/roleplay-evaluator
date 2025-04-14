import time
from unittest.mock import patch

import pytest

from src.utils.retry_utils import retry_with_exponential_backoff


def test_retry_with_exponential_backoff_success():
    """성공적인 실행 테스트"""

    @retry_with_exponential_backoff(max_retries=3)
    def successful_function():
        return "success"

    result = successful_function()
    assert result == "success"


def test_retry_with_exponential_backoff_failure():
    """실패 후 재시도 테스트"""
    attempts = 0

    @retry_with_exponential_backoff(max_retries=3, initial_delay=0.1)
    def failing_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception("Temporary failure")
        return "success"

    result = failing_function()
    assert result == "success"
    assert attempts == 3


def test_retry_with_exponential_backoff_max_retries():
    """최대 재시도 횟수 초과 테스트"""
    attempts = 0

    @retry_with_exponential_backoff(max_retries=3, initial_delay=0.1)
    def always_failing_function():
        nonlocal attempts
        attempts += 1
        raise Exception("Always failing")

    with pytest.raises(Exception) as exc_info:
        always_failing_function()

    assert str(exc_info.value) == "Always failing"
    assert attempts == 3


def test_retry_with_exponential_backoff_delay():
    """지연 시간 테스트"""
    attempts = 0
    start_time = time.time()

    @retry_with_exponential_backoff(max_retries=3, initial_delay=0.1)
    def failing_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise Exception("Temporary failure")
        return "success"

    failing_function()
    elapsed_time = time.time() - start_time

    # 지연 시간이 적절한지 확인 (초기 지연 0.1초, 두 번째 시도 0.2초)
    assert elapsed_time >= 0.3  # 0.1 + 0.2 = 0.3초 이상 소요되어야 함


# def test_retry_with_exponential_backoff_jitter():
#     """지터(jitter) 테스트"""
#     attempts = 0
#     delays = []

#     @retry_with_exponential_backoff(max_retries=3, initial_delay=0.1, jitter=True)
#     def failing_function():
#         nonlocal attempts
#         attempts += 1
#         if attempts < 3:
#             raise Exception("Temporary failure")
#         return "success"

#     with patch("time.sleep") as mock_sleep:

#         def sleep_side_effect(delay):
#             delays.append(delay)

#         mock_sleep.side_effect = sleep_side_effect

#         failing_function()

#     # 지터가 적용되어 지연 시간이 변동되는지 확인
#     assert len(delays) == 2  # 2번의 재시도
#     assert delays[0] != delays[1]  # 지연 시간이 다름
#     assert all(0.05 <= delay <= 0.2 for delay in delays)  # 지터 범위 내

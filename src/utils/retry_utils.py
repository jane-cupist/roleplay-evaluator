import random
import time
from functools import wraps
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
) -> Callable:
    """
    지수 백오프를 사용하여 함수를 재시도하는 데코레이터

    Args:
        max_retries: 최대 재시도 횟수
        initial_delay: 초기 지연 시간 (초)
        max_delay: 최대 지연 시간 (초)
        exponential_base: 지수 백오프의 기본값
        jitter: 지연 시간에 랜덤성을 추가할지 여부
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_retries - 1:
                        raise last_exception

                    # 지연 시간 계산
                    delay = min(delay * exponential_base, max_delay)
                    if jitter:
                        delay = delay * (0.5 + random.random())

                    time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator

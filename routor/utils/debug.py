import logging
import time
from typing import Any, Callable, TypeVar, cast

logger = logging.getLogger()

Func = TypeVar('Func', bound=Callable[..., Any])


def timeit(func: Func) -> Func:
    """
    Measure and log execution time of the decorated function.
    """

    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.debug(f"{func.__qualname__}: {end - start} s")
        return result

    return cast(Func, wrapper)

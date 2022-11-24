import logging
import time
from typing import Callable


def timer(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        logging.info(f"Время выполнения {int(time.time()-time_start)} секунд")
        return result
    return wrapper

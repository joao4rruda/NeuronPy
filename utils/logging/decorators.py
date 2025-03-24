import time
from functools import wraps
from .logger import default_logger

def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        default_logger.info(f"Função chamada: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start
        default_logger.info(f"{func.__name__} executou em {duration:.4f}s")
        return result
    return wrapper

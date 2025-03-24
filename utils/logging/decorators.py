import logging
import time
from functools import wraps
from typing import Callable, Any, Optional
from ..logger import default_logger


def log_function_call(logger: logging.Logger = default_logger,
                      level: int = logging.DEBUG):
    """
    Decorador para registrar chamadas de função

    Args:
        logger: Instância do logger a ser usado
        level: Nível de log para registrar a chamada
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger.log(
                level,
                f"Chamando {func.__qualname__}",
                extra={
                    'args': args,
                    'kwargs': kwargs,
                    'function': func.__name__,
                    'module': func.__module__
                }
            )

            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                exec_time = time.time() - start_time

                logger.log(
                    level,
                    f"Função {func.__qualname__} concluída em {exec_time:.2f}s",
                    extra={
                        'execution_time': exec_time,
                        'result': str(result)[:200]  # Limita tamanho do log
                    }
                )
                return result
            except Exception as e:
                logger.error(
                    f"Erro em {func.__qualname__}: {str(e)}",
                    exc_info=True,
                    extra={
                        'error_type': type(e).__name__,
                        'function': func.__name__,
                        'module': func.__module__
                    }
                )
                raise

        return wrapper

    return decorator


def log_execution_time(logger: logging.Logger = default_logger,
                       threshold: float = 1.0):
    """
    Decorador para registrar tempo de execução de funções

    Args:
        logger: Instância do logger a ser usado
        threshold: Tempo mínimo em segundos para registrar
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            result = func(*args, **kwargs)
            exec_time = time.time() - start_time

            if exec_time >= threshold:
                logger.warning(
                    f"Função {func.__qualname__} lenta: {exec_time:.2f}s",
                    extra={
                        'execution_time': exec_time,
                        'threshold': threshold,
                        'function': func.__name__,
                        'module': func.__module__
                    }
                )
            return result

        return wrapper

    return decorator
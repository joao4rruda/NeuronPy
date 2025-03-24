import logging
import json
from typing import Any, Dict
from colorama import Fore, Style


class JSONFormatter(logging.Formatter):
    """Formata logs como JSON estruturado"""

    def format(self, record: logging.LogRecord) -> str:
        """Formata o registro de log como JSON"""
        log_record = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }

        # Adiciona campos extras
        if hasattr(record, 'extra'):
            log_record.update(record.extra)

        # Adiciona informação de exceção se existir
        if record.exc_info:
            log_record['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_record, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """Formata logs com cores para o console"""

    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def format(self, record: logging.LogRecord) -> str:
        """Formata o registro de log com cores"""
        color = self.COLORS.get(record.levelname, Fore.WHITE)
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"
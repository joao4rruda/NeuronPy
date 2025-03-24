import logging
from typing import Dict, Any
from selenium.common.exceptions import WebDriverException
from openai import OpenAIError


class SeleniumHandler(logging.Handler):
    """Handler especial para eventos do Selenium"""

    def emit(self, record: logging.LogRecord):
        """Processa eventos específicos do Selenium"""
        if hasattr(record, 'selenium_event'):
            self._process_selenium_event(record)
        super().emit(record)

    def _process_selenium_event(self, record: logging.LogRecord):
        """Formata mensagens de log do Selenium"""
        extra: Dict[str, Any] = getattr(record, 'extra', {})

        record.msg = f"Selenium Event - {record.msg}"
        if 'page_url' in extra:
            record.msg += f" | URL: {extra['page_url']}"
        if 'element_locator' in extra:
            record.msg += f" | Locator: {extra['element_locator']}"


class OpenAIHandler(logging.Handler):
    """Handler especial para eventos da OpenAI"""

    def emit(self, record: logging.LogRecord):
        """Processa eventos específicos da OpenAI"""
        if record.exc_info and isinstance(record.exc_info[1], OpenAIError):
            self._process_openai_error(record)
        super().emit(record)

    def _process_openai_error(self, record: logging.LogRecord):
        """Formata mensagens de erro da OpenAI"""
        extra: Dict[str, Any] = getattr(record, 'extra', {})

        record.msg = f"OpenAI Error - {record.msg}"
        if 'model_used' in extra:
            record.msg += f" | Model: {extra['model_used']}"
        if 'parameters' in extra:
            record.msg += f" | Params: {str(extra['parameters'])[:100]}..."
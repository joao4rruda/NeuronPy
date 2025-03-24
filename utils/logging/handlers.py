import logging
from typing import Dict, Any
from selenium.common.exceptions import WebDriverException
from openai import OpenAIError

class SeleniumHandler(logging.Handler):
    """Handler especial para eventos do Selenium."""

    def emit(self, record: logging.LogRecord):
        if hasattr(record, 'selenium_event'):
            self._process_selenium_event(record)
        log_entry = self.format(record)
        print(f"[SeleniumHandler] {log_entry}")

    def _process_selenium_event(self, record: logging.LogRecord):
        extra: Dict[str, Any] = getattr(record, 'extra', {})
        record.msg = f"Selenium Event - {record.msg}"
        if 'page_url' in extra:
            record.msg += f" | URL: {extra['page_url']}"
        if 'element_locator' in extra:
            record.msg += f" | Locator: {extra['element_locator']}"

class OpenAIHandler(logging.Handler):
    """Handler especial para eventos da OpenAI."""

    def emit(self, record: logging.LogRecord):
        if hasattr(record, 'openai_event'):
            self._process_openai_error(record)
        log_entry = self.format(record)
        print(f"[OpenAIHandler] {log_entry}")

    def _process_openai_error(self, record: logging.LogRecord):
        extra: Dict[str, Any] = getattr(record, 'extra', {})
        record.msg = f"OpenAI Error - {record.msg}"
        if 'model_used' in extra:
            record.msg += f" | Model: {extra['model_used']}"
        if 'parameters' in extra:
            record.msg += f" | Params: {str(extra['parameters'])[:100]}..."

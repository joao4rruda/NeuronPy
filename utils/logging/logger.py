import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

class NeuronLogger:
    def __init__(self, name: str = "neuronpy", log_level: str = "INFO",
                 log_file: Optional[str] = None, enable_console: bool = True,
                 json_format: bool = False, enable_handlers: bool = True):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level.upper())
        self.logger.propagate = False

        self._clear_existing_handlers()
        formatter = self._get_formatter(json_format)
        self._setup_handlers(formatter, log_file, enable_console)

        if enable_handlers:
            self._setup_special_handlers()

        sys.excepthook = self._handle_uncaught_exception
        self.logger.info("Logger configurado com sucesso")

    def _clear_existing_handlers(self):
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

    def _get_formatter(self, json_format: bool) -> logging.Formatter:
        if json_format:
            try:
                from .formatters import JSONFormatter
                return JSONFormatter()
            except ImportError:
                self.logger.warning("Formato JSON não pôde ser carregado. Usando formatter padrão.")
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def _setup_handlers(self, formatter: logging.Formatter,
                        log_file: Optional[str], enable_console: bool):
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if log_file:
            self._setup_file_handler(log_file, formatter)

    def _setup_file_handler(self, log_file: str, formatter: logging.Formatter):
        from logging.handlers import RotatingFileHandler
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _setup_special_handlers(self):
        try:
            from .handlers import SeleniumHandler, OpenAIHandler
            self.logger.addHandler(SeleniumHandler())
            self.logger.addHandler(OpenAIHandler())
        except ImportError as e:
            self.logger.warning(f"Handlers especiais não carregados: {e}")

    def _handle_uncaught_exception(self, exc_type, exc_value, exc_traceback):
        self.logger.error(
            "Exceção não tratada ocorreu",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    def get_logger(self) -> logging.Logger:
        return self.logger

default_logger = NeuronLogger().get_logger()

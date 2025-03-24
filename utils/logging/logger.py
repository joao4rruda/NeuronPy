import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import json


class NeuronLogger:
    def __init__(self, name: str = "neuronpy", log_level: str = "INFO",
                 log_file: Optional[str] = None, enable_console: bool = True,
                 json_format: bool = False, enable_handlers: bool = True):
        """
        Configuração completa do sistema de logging

        Args:
            name: Nome do logger
            log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Caminho para arquivo de log (opcional)
            enable_console: Se True, habilita logging no console
            json_format: Se True, usa formato JSON para logs
            enable_handlers: Se True, habilita handlers especiais
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level.upper())

        # Evita propagação para o root logger
        self.logger.propagate = False

        # Remove handlers existentes
        self._clear_existing_handlers()

        # Configura formatação
        formatter = self._get_formatter(json_format)

        # Configura handlers
        self._setup_handlers(formatter, log_file, enable_console)

        # Handlers especiais
        if enable_handlers:
            self._setup_special_handlers()

        # Captura de exceções não tratadas
        sys.excepthook = self._handle_uncaught_exception

        # Log inicial
        self.logger.info("Logger configurado com sucesso")

    def _clear_existing_handlers(self):
        """Remove todos os handlers existentes"""
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

    def _get_formatter(self, json_format: bool) -> logging.Formatter:
        """Retorna o formatter apropriado"""
        if json_format:
            from .formatters import JSONFormatter
            return JSONFormatter()
        else:
            return logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )

    def _setup_handlers(self, formatter: logging.Formatter,
                        log_file: Optional[str], enable_console: bool):
        """Configura os handlers básicos"""
        if enable_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

        if log_file:
            self._setup_file_handler(log_file, formatter)

    def _setup_file_handler(self, log_file: str, formatter: logging.Formatter):
        """Configura handler para arquivo com rotação"""
        from logging.handlers import RotatingFileHandler
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _setup_special_handlers(self):
        """Configura handlers especiais para Selenium e OpenAI"""
        from .handlers import SeleniumHandler, OpenAIHandler
        self.logger.addHandler(SeleniumHandler())
        self.logger.addHandler(OpenAIHandler())

    def _handle_uncaught_exception(self, exc_type, exc_value, exc_traceback):
        """Captura exceções não tratadas"""
        self.logger.error(
            "Exceção não tratada ocorreu",
            exc_info=(exc_type, exc_value, exc_traceback)
        )

    def get_logger(self) -> logging.Logger:
        """Retorna o logger configurado"""
        return self.logger


# Logger global padrão
default_logger = NeuronLogger().get_logger()
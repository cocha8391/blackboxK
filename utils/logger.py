"""
Sistema de logging para debuggeo y monitoreo de la aplicación.
Facilita entender qué ocurre en cada parte del código.
"""

import logging
import os
from datetime import datetime

from utils.constants import LOG_FILE


class Logger:
    """
    Gestor de logging centralizado.
    Proporciona métodos para registrar eventos, errores y debug.
    """

    _instance = None

    def __new__(cls):
        """Patrón Singleton - solo una instancia del logger."""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Inicializa el logger si no está ya inicializado."""
        if self._initialized:
            return

        self._initialized = True

        # Crear logger
        self.logger = logging.getLogger("BlackBoxK")
        self.logger.setLevel(logging.DEBUG)

        # Formato: [TIMESTAMP] [LEVEL] [COMPONENT] - Mensaje
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # Handler: archivo
        try:
            file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"No se pudo crear logger de archivo: {e}")

        # Handler: consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def debug(self, component: str, message: str):
        """Registra mensaje de debug (detalles internos)."""
        self.logger.debug(f"[{component}] {message}")

    def info(self, component: str, message: str):
        """Registra mensaje informativo."""
        self.logger.info(f"[{component}] {message}")

    def warning(self, component: str, message: str):
        """Registra advertencia."""
        self.logger.warning(f"[{component}] {message}")

    def error(self, component: str, message: str, exception: Exception = None):
        """Registra error."""
        if exception:
            self.logger.error(f"[{component}] {message}", exc_info=exception)
        else:
            self.logger.error(f"[{component}] {message}")

    def critical(self, component: str, message: str):
        """Registra error crítico."""
        self.logger.critical(f"[{component}] {message}")


# Instancia global del logger
_logger_instance = Logger()


def get_logger():
    """Retorna la instancia del logger."""
    return _logger_instance

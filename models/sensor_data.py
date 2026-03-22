"""
Gestor de datos de sensores.
Mantiene el estado actual de todos los sensores en memoria.
"""

from threading import Lock

from utils.constants import PRESSURE_KEYS, TEMPERATURE_KEYS
from utils.logger import get_logger

logger = get_logger()


class SensorData:
    """
    Almacena el estado actual de sensores de forma thread-safe.
    Proporciona acceso atomático a valores de presión y temperatura.
    """

    def __init__(self):
        """Inicializa con valores en cero."""
        self._lock = Lock()

        # Inicializar sensores con valor 0
        self._sensor_values = {}
        for key in PRESSURE_KEYS + TEMPERATURE_KEYS:
            self._sensor_values[key] = 0.0

        logger.info("SensorData", "Sistema de sensores inicializado")

    def update(self, key: str, value: float) -> None:
        """
        Actualiza el valor de un sensor específico.

        Args:
            key: Identificador del sensor (P1, P2, T1, T2, etc)
            value: Nuevo valor del sensor
        """
        with self._lock:
            if key in self._sensor_values:
                self._sensor_values[key] = round(value, 1)
                logger.debug("SensorData", f"{key} = {value}")
            else:
                logger.warning("SensorData", f"Sensor desconocido: {key}")

    def get(self, key: str) -> float:
        """
        Obtiene el valor actual de un sensor.

        Args:
            key: Identificador del sensor

        Returns:
            float: Valor actual del sensor (0 si no existe)
        """
        with self._lock:
            return self._sensor_values.get(key, 0.0)

    def get_all(self) -> dict:
        """
        Obtiene un snapshot de todos los sensores.

        Returns:
            dict: Copia de todos los valores de sensores
        """
        with self._lock:
            return dict(self._sensor_values)

    def get_pressures(self) -> dict:
        """Retorna solo los valores de presión."""
        with self._lock:
            return {k: self._sensor_values[k] for k in PRESSURE_KEYS}

    def get_temperatures(self) -> dict:
        """Retorna solo los valores de temperatura."""
        with self._lock:
            return {k: self._sensor_values[k] for k in TEMPERATURE_KEYS}

    def reset(self) -> None:
        """Reinicia todos los sensores a cero."""
        with self._lock:
            for key in self._sensor_values:
                self._sensor_values[key] = 0.0
        logger.info("SensorData", "Sensores reseteados a 0")

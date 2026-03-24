"""
Data Logger - Recolección y exportación de datos de sensores.
Almacena datos cada 2 segundos y exporta a CSV mensual.
"""

import csv
import os
from datetime import datetime
from threading import Lock
from typing import List, Dict

from utils.constants import PRESSURE_KEYS, TEMPERATURE_KEYS
from utils.logger import get_logger

logger = get_logger()


class DataLogger:
    """
    Recoge datos de sensores y los exporta a archivos CSV mensuales.
    """

    def __init__(self, export_dir: str = "exports"):
        """
        Inicializa el data logger.

        Args:
            export_dir: Directorio para exportar archivos CSV
        """
        self.export_dir = export_dir
        self._lock = Lock()
        self.records: List[Dict] = []
        self.current_month = datetime.now().strftime("%Y_%m")

        # Crear directorio si no existe
        os.makedirs(self.export_dir, exist_ok=True)

        logger.info("DataLogger", f"Inicializado. Directorio de exportación: {self.export_dir}")

    def log_sensor_data(self, sensor_key: str, value: float) -> None:
        """
        Registra un dato de sensor.

        Args:
            sensor_key: Clave del sensor (P1, T1, etc.)
            value: Valor del sensor
        """
        timestamp = datetime.now().isoformat()
        record = {
            "timestamp": timestamp,
            "sensor": sensor_key,
            "value": round(value, 2)
        }

        with self._lock:
            self.records.append(record)

        logger.debug("DataLogger", f"Registrado: {sensor_key} = {value}")

    def check_and_export_monthly(self) -> None:
        """
        Verifica si cambió el mes y exporta datos si es necesario.
        """
        current_month = datetime.now().strftime("%Y_%m")

        if current_month != self.current_month:
            self._export_to_csv()
            self.current_month = current_month
            with self._lock:
                self.records = []  # Resetear registros

    def _export_to_csv(self) -> None:
        """
        Exporta los registros actuales a un archivo CSV.
        """
        if not self.records:
            logger.info("DataLogger", "No hay registros para exportar")
            return

        filename = f"data_{self.current_month}.csv"
        filepath = os.path.join(self.export_dir, filename)

        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['timestamp', 'sensor', 'value']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.records)

            logger.info("DataLogger", f"Datos exportados a {filepath}. Registros: {len(self.records)}")

        except Exception as e:
            logger.error("DataLogger", f"Error exportando datos: {e}", exception=e)

    def get_record_count(self) -> int:
        """
        Obtiene el número de registros actuales.

        Returns:
            int: Número de registros
        """
        with self._lock:
            return len(self.records)

    def is_export_ready(self) -> bool:
        """
        Verifica si el directorio de exportación es válido y escribible.

        Returns:
            bool: True si está listo
        """
        try:
            if not os.path.isdir(self.export_dir):
                return False
            return os.access(self.export_dir, os.W_OK)
        except Exception:
            return False

    def force_export(self) -> None:
        """
        Fuerza la exportación de datos actuales (para pruebas o cierre).
        """
        self._export_to_csv()
        with self._lock:
            self.records = []
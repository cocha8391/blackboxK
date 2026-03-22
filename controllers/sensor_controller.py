"""
Controlador de sensores - Lee del hardware y convierte a unidades de usuario.
"""

from models.hardware_manager import HardwareManager
from models.sensor_data import SensorData
from utils.constants import NUM_PRESSURE_SENSORS, NUM_TEMPERATURE_SENSORS, PRESSURE_KEYS, TEMPERATURE_KEYS
from utils.converters import adc_to_uservalue
from utils.logger import get_logger

logger = get_logger()


class SensorController:
    """
    Controlador de sensores.
    Lee datos analógicos del hardware, convierte 4-20mA a unidades de usuario,
    y actualiza el estado en SensorData.
    """

    def __init__(self, hardware_manager: HardwareManager, sensor_data: SensorData, config: dict):
        """
        Inicializa el controlador de sensores.

        Args:
            hardware_manager: Gestor del hardware (lectura ADC)
            sensor_data: Almacén de estado de sensores
            config: Diccionario de configuración (inputs)
        """
        self.hardware = hardware_manager
        self.sensor_data = sensor_data
        self.config_inputs = config

        logger.info("SensorController", "Inicializado")

    def read_all_sensors(self) -> None:
        """
        Lee todos los sensores (presión + temperatura) y actualiza SensorData.

        Flujo:
        1. Leer canal ADC (hardware)
        2. Convertir ADC → mA → Unidades usuario (usando converters)
        3. Actualizar SensorData

        Esta función se ejecuta periódicamente (cada 500ms típicamente).
        """
        # Leer presiones (canales 0-3)
        for i in range(NUM_PRESSURE_SENSORS):
            key = PRESSURE_KEYS[i]
            self._read_sensor(key, channel=i)

        # Leer temperaturas (canales 4-7)
        for i in range(NUM_TEMPERATURE_SENSORS):
            key = TEMPERATURE_KEYS[i]
            self._read_sensor(key, channel=i + 4)

    def _read_sensor(self, key: str, channel: int) -> None:
        """
        Lee un sensor específico.

        Args:
            key: Identificador del sensor (P1, P2, T1, T2, etc)
            channel: Número de canal analógico (0-7)
        """
        try:
            # Obtener configuración del sensor
            sensor_config = self.config_inputs.get(key, {})
            min_val = sensor_config.get("min", 0)
            max_val = sensor_config.get("max", 100)

            # Leer ADC del hardware
            adc_val = self.hardware.read_analog_channel(channel)

            # Convertir ADC a unidades de usuario
            user_value = adc_to_uservalue(adc_val, min_val, max_val)

            # Actualizar estado
            self.sensor_data.update(key, user_value)

        except Exception as e:
            logger.error(
                "SensorController",
                f"Error leyendo sensor {key}: {e}",
                exception=e,
            )

    def get_sensor_value(self, key: str) -> float:
        """
        Obtiene el valor actual de un sensor.

        Args:
            key: Identificador del sensor

        Returns:
            float: Valor en unidades de usuario
        """
        return self.sensor_data.get(key)

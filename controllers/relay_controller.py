"""
Controlador de relés - Evalúa lógica y controla salidas.
"""

from models.hardware_manager import HardwareManager
from models.sensor_data import SensorData
from utils.constants import NUM_RELAYS, RELAY_KEYS
from utils.logger import get_logger

logger = get_logger()


class RelayController:
    """
    Controlador de relés.
    Evalúa la lógica de cada relé (comparación con setpoint) y escribe salidas.
    """

    def __init__(self, hardware_manager: HardwareManager, sensor_data: SensorData, config: dict):
        """
        Inicializa el controlador de relés.

        Args:
            hardware_manager: Gestor del hardware (escritura SPI)
            sensor_data: Almacén de estado de sensores
            config: Diccionario de configuración (relays)
        """
        self.hardware = hardware_manager
        self.sensor_data = sensor_data
        self.config_relays = config

        # Estado interno de relés (para saber cuál cambió)
        self.relay_state = 0

        logger.info("RelayController", "Inicializado")

    def evaluate_and_write(self) -> int:
        """
        Evalúa todos los relés y escribe en el hardware.

        Flujo:
        1. Para cada relé, obtener su configuración
        2. Comparar valor actual del sensor con setpoint
        3. Determinar si debe estar ON u OFF
        4. Escribir byte de estado en hardware

        Returns:
            int: Byte de estado final de relés
        """
        new_state = 0

        for i in range(NUM_RELAYS):
            relay_key = RELAY_KEYS[i]
            is_active = self._evaluate_relay(relay_key)

            if is_active:
                # Activar bit i
                new_state |= (1 << i)

        # Detectar cambios
        if new_state != self.relay_state:
            logger.info(
                "RelayController",
                f"Cambio de estado: 0x{self.relay_state:02x} → 0x{new_state:02x}",
            )

        # Escribir en hardware
        self.hardware.write_relay_state(new_state)
        self.relay_state = new_state

        return new_state

    def _evaluate_relay(self, relay_key: str) -> bool:
        """
        Evalúa si un relé debe estar activado.

        Lógica:
        - "Pressure Max": Activar si sensor >= setpoint
        - "Pressure Min": Activar si sensor <= setpoint
        - "Temperature Max": Activar si sensor >= setpoint
        - "Temperature Min": Activar si sensor <= setpoint

        Args:
            relay_key: Identificador del relé (relay1, relay2, etc)

        Returns:
            bool: True si debe estar activado, False si inactivo
        """
        try:
            relay_config = self.config_relays.get(relay_key, {})

            # Obtener parámetros de configuración
            channel = relay_config.get("channel", "")
            setpoint = relay_config.get("setpoint", 0)
            function = relay_config.get("function", "")

            # Obtener valor actual del sensor
            sensor_value = self.sensor_data.get(channel)

            # Evaluar lógica
            if "Max" in function and sensor_value >= setpoint:
                return True

            if "Min" in function and sensor_value <= setpoint:
                return True

            return False

        except Exception as e:
            logger.error(
                "RelayController",
                f"Error evaluando relé {relay_key}: {e}",
                exception=e,
            )
            return False

    def get_relay_state(self) -> int:
        """
        Obtiene el estado actual de todos los relés.

        Returns:
            int: Byte con bits de estado (bit i = relay i)
        """
        return self.relay_state

    def is_relay_active(self, relay_index: int) -> bool:
        """
        Obtiene el estado de un relé específico.

        Args:
            relay_index: Índice del relé (0-3)

        Returns:
            bool: True si está activado
        """
        if relay_index < 0 or relay_index >= 4:
            return False
        return bool((self.relay_state >> relay_index) & 1)

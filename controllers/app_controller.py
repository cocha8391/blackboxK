"""
Controlador de aplicación - Orquesta todo el sistema.
Coordina modelos, controladores y vistas.
"""

from models.config_manager import ConfigManager
from models.hardware_manager import HardwareManager
from models.sensor_data import SensorData
from controllers.sensor_controller import SensorController
from controllers.relay_controller import RelayController
from utils.constants import SENSOR_READ_INTERVAL, RELAY_EVAL_INTERVAL
from utils.logger import get_logger

logger = get_logger()


class AppController:
    """
    Controlador principal de la aplicación.

    Responsabilidades:
    - Inicializar y coordinar todos los componentes
    - Orquestar ciclos de lectura de sensores
    - Orquestar ciclos de evaluación de relés
    - Proporcionar acceso unificado a datos y lógica
    """

    def __init__(self, use_hardware_simulation: bool = False):
        """
        Inicializa la aplicación.

        Args:
            use_hardware_simulation: Si True, simula hardware (para Windows)
        """
        logger.info("AppController", "Inicializando aplicación...")

        # Capa de datos
        self.config = ConfigManager()
        self.sensor_data = SensorData()
        self.hardware = HardwareManager(use_simulation=use_hardware_simulation)

        # Capa de lógica
        self.sensor_controller = SensorController(
            self.hardware,
            self.sensor_data,
            self.config.get_inputs(),
        )

        self.relay_controller = RelayController(
            self.config,
            self.hardware,
            self.sensor_data,
        )

        logger.info("AppController", "Aplicación inicializada correctamente")

    def read_sensors(self) -> None:
        """
        Lee todos los sensores y actualiza el estado.
        Se ejecuta periódicamente desde la vista.
        """
        self.sensor_controller.read_all_sensors()

    def evaluate_relays(self) -> int:
        """
        Evalúa la lógica de los relés y escribe en hardware.
        Se ejecuta periódicamente desde la vista.

        Returns:
            int: Byte de estado de relés
        """
        return self.relay_controller.evaluate_and_write()

    def get_sensor_value(self, key: str) -> float:
        """Obtiene el valor de un sensor."""
        return self.sensor_data.get(key)

    def get_all_sensors(self) -> dict:
        """Obtiene todos los valores de sensores."""
        return self.sensor_data.get_all()

    def get_pressures(self) -> dict:
        """Obtiene valores de presión."""
        return self.sensor_data.get_pressures()

    def get_temperatures(self) -> dict:
        """Obtiene valores de temperatura."""
        return self.sensor_data.get_temperatures()

    def get_relay_state(self) -> int:
        """Obtiene el estado de todos los relés."""
        return self.relay_controller.get_relay_state()

    def is_relay_active(self, relay_index: int) -> bool:
        """Obtiene el estado de un relé específico."""
        return self.relay_controller.is_relay_active(relay_index)

    def get_config(self) -> ConfigManager:
        """Obtiene el gestor de configuración."""
        return self.config

    def update_input_config(
        self, key: str, name: str, min_val: float, max_val: float
    ) -> bool:
        """Actualiza la configuración de un sensor."""
        return self.config.update_input(key, name, min_val, max_val)

    def update_relay_config(
        self,
        key: str,
        name: str,
        function: str,
        channel: str,
        setpoint: float,
    ) -> bool:
        """Actualiza la configuración de un relé."""
        return self.config.update_relay(key, name, function, channel, setpoint)

    def shutdown(self) -> None:
        """Limpia recursos y desconecta hardware."""
        logger.info("AppController", "Cerrando aplicación...")
        self.hardware.disconnect()
        logger.info("AppController", "Aplicación cerrada")

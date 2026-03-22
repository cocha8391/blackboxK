"""
Gestor de hardware - Interfaz con módulos SPI.
Proporciona una abstracción que funciona en Windows y Raspberry Pi.
"""

import platform

from utils.constants import SPI_CE0, SPI_CE1
from utils.logger import get_logger

logger = get_logger()


class HardwareManager:
    """
    Gestor centralizado de hardware (módulos SPI).

    En Raspberry Pi:
        - Usa widgetlords para comunicación SPI real
        - Mod8AI (CE0): Lectura analógica
        - Mod4KO (CE1): Salida de relés

    En Windows (desarrollo):
        - Simula los módulos retornando valores ficticios
    """

    def __init__(self, use_simulation: bool = False):
        """
        Inicializa el HardwareManager.

        Args:
            use_simulation: Si True, fuerza simulación. Si False, intenta hardware real.
        """
        self.is_windows = platform.system() == "Windows"
        self.use_simulation = use_simulation or self.is_windows

        if self.use_simulation:
            self._init_simulation()
        else:
            self._init_hardware()

    def _init_simulation(self) -> None:
        """Modo simulación para Windows."""
        self.ai_module = None
        self.relay_module = None
        self.is_connected = True

        logger.info("HardwareManager", "Modo SIMULACIÓN - Sin hardware real")

    def _init_hardware(self) -> None:
        """Modo hardware real para Raspberry Pi."""
        try:
            from widgetlords.pi_spi_din import ChipEnable, Mod4KO, Mod8AI, init

            init()
            self.ai_module = Mod8AI(ChipEnable.CE0)
            self.relay_module = Mod4KO(ChipEnable.CE1)
            self.is_connected = True

            logger.info("HardwareManager", "Hardware real inicializado correctamente")

        except ImportError as e:
            logger.error(
                "HardwareManager",
                "No se pudo importar widgetlords, usando simulación",
                exception=e,
            )
            self._init_simulation()

        except Exception as e:
            logger.error(
                "HardwareManager",
                "Error al inicializar hardware, usando simulación",
                exception=e,
            )
            self._init_simulation()

    def read_analog_channel(self, channel: int) -> int:
        """
        Lee un canal analógico (0-7).

        Args:
            channel: Número de canal (0-7)

        Returns:
            int: Valor ADC crudo (0-4095 típicamente)
        """
        if not self.is_connected or self.ai_module is None:
            # Valor simulado
            return 2000

        try:
            return self.ai_module.read_single(channel)

        except Exception as e:
            logger.error(
                "HardwareManager",
                f"Error leyendo canal analógico {channel}: {e}",
                exception=e,
            )
            return 0

    def write_relay_state(self, relay_byte: int) -> bool:
        """
        Escribe el estado de los 4 relés (bits 0-3).

        Args:
            relay_byte: Byte con estado de relés (bit i = relay i)

        Returns:
            bool: True si se escribió exitosamente
        """
        if not self.is_connected or self.relay_module is None:
            logger.debug("HardwareManager", f"Relés (simulado): 0x{relay_byte:02x}")
            return True

        try:
            self.relay_module.write(relay_byte)
            logger.debug("HardwareManager", f"Relés escritos: 0x{relay_byte:02x}")
            return True

        except Exception as e:
            logger.error(
                "HardwareManager",
                f"Error escribiendo relés: {e}",
                exception=e,
            )
            return False

    def get_relay_bit(self, relay_index: int) -> bool:
        """
        Obtiene el estado de un relé específico.

        Args:
            relay_index: Índice del relé (0-3)

        Returns:
            bool: True si está activado
        """
        if relay_index < 0 or relay_index > 3:
            return False
        # Esta funcionalidad podría expandirse si el hardware lo permite
        return False

    def disconnect(self) -> None:
        """Desconecta/limpia los módulos."""
        self.ai_module = None
        self.relay_module = None
        self.is_connected = False
        logger.info("HardwareManager", "Hardware desconectado")

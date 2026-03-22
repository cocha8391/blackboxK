"""
Gestor de configuración - Carga y guarda relay_config.json.
Centraliza toda la configuración del sistema (sensores, relés, setpoints).
"""

import copy
import json
import os

from utils.constants import CONFIG_FILE, DEFAULT_CONFIG
from utils.logger import get_logger

logger = get_logger()


class ConfigManager:
    """
    Gestor de configuración centralizado.
    Carga relay_config.json, valida contenido y proporciona acceso tipo diccionario.
    """

    def __init__(self):
        """Inicializa el ConfigManager cargando la configuración existente."""
        self.config = self._load_config()
        logger.info("ConfigManager", "Configuración cargada exitosamente")

    def _load_config(self) -> dict:
        """
        Carga relay_config.json del disco.

        Si el archivo no existe o está incompleto, usa la configuración por defecto.

        Returns:
            dict: Configuración válida
        """
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Validar que tenga estructura mínima
                if "inputs" in data and "relays" in data:
                    logger.debug(
                        "ConfigManager", f"Config cargada desde {CONFIG_FILE}"
                    )
                    return data
                else:
                    logger.warning(
                        "ConfigManager",
                        "Config incompleta, usando config por defecto",
                    )
                    return copy.deepcopy(DEFAULT_CONFIG)

            except json.JSONDecodeError as e:
                logger.error(
                    "ConfigManager",
                    f"Error al parsear JSON: {e}",
                    exception=e,
                )
                return copy.deepcopy(DEFAULT_CONFIG)

            except Exception as e:
                logger.error(
                    "ConfigManager",
                    f"Error al leer {CONFIG_FILE}: {e}",
                    exception=e,
                )
                return copy.deepcopy(DEFAULT_CONFIG)

        else:
            logger.info(
                "ConfigManager",
                f"{CONFIG_FILE} no existe, creando con config por defecto",
            )
            self.save_config()
            return copy.deepcopy(DEFAULT_CONFIG)

    def save_config(self) -> bool:
        """
        Guarda la configuración actual a relay_config.json.

        Returns:
            bool: True si se guardó exitosamente, False si hay error
        """
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)

            logger.info("ConfigManager", "Configuración guardada exitosamente")
            return True

        except Exception as e:
            logger.error(
                "ConfigManager",
                f"Error al guardar {CONFIG_FILE}: {e}",
                exception=e,
            )
            return False

    def get_inputs(self) -> dict:
        """Retorna el diccionario de inputs (sensores)."""
        return self.config.get("inputs", {})

    def get_relays(self) -> dict:
        """Retorna el diccionario de relés."""
        return self.config.get("relays", {})

    def get_input(self, key: str) -> dict:
        """
        Obtiene la configuración de un sensor específico.

        Args:
            key: Identificador del sensor (ej: "P1", "T2")

        Returns:
            dict: Configuración del sensor o {} si no existe
        """
        return self.get_inputs().get(key, {})

    def get_relay(self, key: str) -> dict:
        """
        Obtiene la configuración de un relé específico.

        Args:
            key: Identificador del relé (ej: "relay1", "relay4")

        Returns:
            dict: Configuración del relé o {} si no existe
        """
        return self.get_relays().get(key, {})

    def update_input(self, key: str, name: str, min_val: float, max_val: float) -> bool:
        """
        Actualiza la configuración de un sensor.

        Args:
            key: Identificador del sensor
            name: Nuevo nombre
            min_val: Nuevo valor mínimo
            max_val: Nuevo valor máximo

        Returns:
            bool: True si se actualizó exitosamente
        """
        try:
            if key not in self.config["inputs"]:
                logger.warning(
                    "ConfigManager", f"Input {key} no existe"
                )
                return False

            self.config["inputs"][key]["name"] = str(name).strip()
            self.config["inputs"][key]["min"] = float(min_val)
            self.config["inputs"][key]["max"] = float(max_val)

            logger.info(
                "ConfigManager",
                f"Input {key} actualizado: {name} ({min_val}-{max_val})",
            )
            return self.save_config()

        except ValueError as e:
            logger.error(
                "ConfigManager",
                f"Valores inválidos para input {key}: {e}",
                exception=e,
            )
            return False

    def update_relay(
        self,
        key: str,
        name: str,
        function: str,
        channel: str,
        setpoint: float,
    ) -> bool:
        """
        Actualiza la configuración de un relé.

        Args:
            key: Identificador del relé
            name: Nuevo nombre
            function: Nueva función ("Pressure Max", etc)
            channel: Nuevo canal (sensor que controla)
            setpoint: Nuevo valor de setpoint

        Returns:
            bool: True si se actualizó exitosamente
        """
        try:
            if key not in self.config["relays"]:
                logger.warning(
                    "ConfigManager", f"Relay {key} no existe"
                )
                return False

            self.config["relays"][key]["name"] = str(name).strip()
            self.config["relays"][key]["function"] = str(function).strip()
            self.config["relays"][key]["channel"] = str(channel).strip()
            self.config["relays"][key]["setpoint"] = float(setpoint)

            logger.info(
                "ConfigManager",
                f"Relay {key} actualizado: {name} ({function} @ {setpoint})",
            )
            return self.save_config()

        except ValueError as e:
            logger.error(
                "ConfigManager",
                f"Valores inválidos para relay {key}: {e}",
                exception=e,
            )
            return False

    def reset_to_default(self) -> bool:
        """
        Reseta la configuración a los valores por defecto.

        Returns:
            bool: True si se guardó exitosamente
        """
        self.config = copy.deepcopy(DEFAULT_CONFIG)
        logger.info("ConfigManager", "Configuración reseteada a valores por defecto")
        return self.save_config()

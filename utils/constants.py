"""
Constantes compartidas en toda la aplicación.
Centraliza valores que se usan en múltiples módulos.
"""

# ===== INTERFAZ =====
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 480
FULLSCREEN_MODE = True  # Cambiar a True para Raspberry Pi

# ===== COLORES =====
COLOR_PRIMARY = "#007acc"      # Azul principal
COLOR_SUCCESS = "#28a745"      # Verde
COLOR_DANGER = "#cc0000"       # Rojo
COLOR_BG_MAIN = "white"        # Fondo principal
COLOR_BG_PAGE = "#e9eef3"      # Fondo páginas sensores
COLOR_BG_DIALOG = "#f5f5f5"    # Fondo diálogos

# Color relé ON/OFF
COLOR_RELAY_ON = "#c8f7c5"     # Verde claro
COLOR_RELAY_OFF = "white"      # Blanco

TEXT_COLOR_RELAY_ON = "green"
TEXT_COLOR_RELAY_OFF = "gray"

# ===== FRECUENCIAS (ms) =====
SENSOR_READ_INTERVAL = 2000     # Lectura sensores cada 2000ms (2 segundos)
RELAY_EVAL_INTERVAL = 500      # Evaluación relés cada 500ms
HOLD_CONFIG_TIME = 15000       # 15 segundos para abrir configuración

# ===== CONVERSIÓN 4-20mA =====
# Calibración ADC a mA (valores de widgetlords)
ADC_MIN = 745      # Valor ADC para 4mA
ADC_MAX = 3723     # Valor ADC para 20mA
MA_MIN = 4         # Corriente mínima
MA_MAX = 20        # Corriente máxima

# ===== HARDWARE =====
# Direcciones SPI
SPI_CE0 = 0        # Chip Enable 0 - Módulo Analog Input (Mod8AI)
SPI_CE1 = 1        # Chip Enable 1 - Módulo Relay Output (Mod4KO)

# ===== SENSORES (ENTRADA ANALÓGICA) =====
NUM_PRESSURE_SENSORS = 4
NUM_TEMPERATURE_SENSORS = 4
TOTAL_ANALOG_CHANNELS = 8

PRESSURE_KEYS = ["P1", "P2", "P3", "P4"]
TEMPERATURE_KEYS = ["T1", "T2", "T3", "T4"]

PRESSURE_UNIT = "PSI"
TEMPERATURE_UNIT = "°C"

# ===== RELÉS (SALIDA DIGITAL) =====
NUM_RELAYS = 4
RELAY_KEYS = ["relay1", "relay2", "relay3", "relay4"]

# Funciones de relé disponibles
RELAY_FUNCTIONS = [
    "Pressure Max",
    "Pressure Min",
    "Temperature Max",
    "Temperature Min",
    "Control Manual"
]

# ===== CONFIGURACIÓN POR DEFECTO =====
DEFAULT_CONFIG = {
    "export_dir": "exports",  # Directorio para exportar datos CSV
    "inputs": {
        "P1": {"name": "Pressure 1", "min": 0, "max": 232},
        "P2": {"name": "Pressure 2", "min": 0, "max": 232},
        "P3": {"name": "Pressure 3", "min": 0, "max": 232},
        "P4": {"name": "Pressure 4", "min": 0, "max": 232},
        "T1": {"name": "Temperature 1", "min": -10, "max": 100},
        "T2": {"name": "Temperature 2", "min": -10, "max": 100},
        "T3": {"name": "Temperature 3", "min": -10, "max": 100},
        "T4": {"name": "Temperature 4", "min": -10, "max": 100},
    },
    "relays": {
        "relay1": {
            "name": "Relay 1",
            "function": "Pressure Max",
            "channel": "P1",
            "setpoint": 0,
        },
        "relay2": {
            "name": "Relay 2",
            "function": "Pressure Max",
            "channel": "P2",
            "setpoint": 0,
        },
        "relay3": {
            "name": "Relay 3",
            "function": "Pressure Max",
            "channel": "P3",
            "setpoint": 0,
        },
        "relay4": {
            "name": "Relay 4",
            "function": "Pressure Max",
            "channel": "P4",
            "setpoint": 0,
        },
    },
}

# ===== PÁGINAS =====
PAGE_SPLASH = 0
PAGE_PRESSURE = 1
PAGE_TEMPERATURE = 2
PAGE_RELAY = 3
PAGE_CONFIG_MENU = 4
PAGE_INPUT_CONFIG = 5
PAGE_RELAY_CONFIG = 6
PAGE_CONNECTIVITY = 7
PAGE_INFO = 8
PAGE_CONFIG_ITEM = 9
TOTAL_PAGES = 10

# ===== ARCHIVOS =====
CONFIG_FILE = "relay_config.json"
LOG_FILE = "blackbox.log"

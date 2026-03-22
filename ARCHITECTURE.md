# ARQUITECTURA MVC - BlackBox K Dashboard

## Resumen Ejecutivo

La aplicación sigue el patrón **Model-View-Controller (MVC)** para separar:
- **MODELS**: Datos, configuración, estado (sensores, hardware)
- **CONTROLLERS**: Lógica de negocio (lectura sensores, evaluación relés, navegación)
- **VIEWS**: Interfaz de usuario (Tkinter, diálogos, eventos)

Esta separación permite que el código sea **fácil de entender, mantener y testear**.

---

## Estructura de Carpetas

```
blackbox-k/
├── main.py                          # 🎬 PUNTO DE ENTRADA
│
├── models/                          # 📊 DATOS Y ESTADO
│   ├── config_manager.py           # Carga/guarda relay_config.json
│   ├── sensor_data.py              # Estado actual de sensores
│   └── hardware_manager.py         # Interfaz con SPI (simula en Windows)
│
├── controllers/                     # 🧠 LÓGICA DE NEGOCIO
│   ├── app_controller.py           # Orquestación principal
│   ├── sensor_controller.py        # Lee y convierte sensores
│   ├── relay_controller.py         # Evalúa lógica de relés
│   └── navigation.py               # Gesiona swipes/páginas
│
├── views/                           # 🎨 INTERFAZ DE USUARIO
│   ├── main_window.py              # Ventana y canvas principal
│   ├── splash_page.py              # Pantalla de inicio
│   ├── sensor_page.py              # Páginas de sensores
│   ├── relay_page.py               # Página de relés
│   └── config_dialogs.py           # Diálogos de configuración
│
├── utils/                           # 🛠️ UTILIDADES
│   ├── constants.py                # Constantes (colores, tamaños, defaults)
│   ├── logger.py                   # Sistema de logging
│   └── converters.py               # Conversión 4-20mA a unidades usuario
│
├── relay_config.json               # Configuración del sistema (generado)
├── blackbox.log                    # Log de ejecución (generado)
├── requirements.txt                # Dependencias
└── README.md                       # Documentación de usuario
```

---

## Flujo de Datos

### 📥 ENTRADA (Lectura de Sensores)

```
Si modo REAL (Raspberry Pi):
    HARDWARE SPI → Lee valores reales de Mod8AI (4-20mA)
Si modo SIMULACION (Windows):
    random.randint(700, 3800) → Simula valores ADC
    ↓
HardwareManager.read_analog_channel() → Retorna 0-4095
    ↓
converters.adc_to_uservalue() → Convierte a unidades usuario
    ↓
[Valor en unidades de usuario: 23.5 PSI, 45.2 °C]
    ↓
SensorData.update(key, value)
    ↓
SensorData._sensor_values["P1"] = 23.5
```

**En Windows:** Los valores de sensores son aleatorios (simulación), perfecto para desarrollo sin hardware real.

**Quién ejecuta esto:**
- `SensorController.read_all_sensors()` (cada 500ms)

---

### ⚙️ LÓGICA (Evaluación de Relés)

```
SensorData (Valores actuales: P1=23.5)
    ↓
RelayController._evaluate_relay("relay1")
    ↓
Config["relay1"] = {
    "channel": "P1",
    "function": "Pressure Max",
    "setpoint": 25.0
}
    ↓
Comparar: P1 (23.5) >= Setpoint (25.0) ?
    ↓
NO → Relay OFF (bit=0)
    ↓
RelayState = 0b0000
```

**Quién ejecuta esto:**
- `RelayController.evaluate_and_write()` (cada 500ms)

---

### 📤 SALIDA (Escritura de Hardware)

```
RelayState = 0b0101  (relés 0 y 2 activados)
    ↓
HardwareManager.write_relay_state(0b0101)
    ↓
Si modo REAL (Raspberry Pi):
    relay_module.write(0b0101) → HARDWARE SPI
Si modo SIMULACION (Windows):
    logger.info("Relay state: 0b0101") → Solo LOG
```

**En Windows:** Los cambios de relés se registran en los logs, sin realizar cambios reales de hardware (porque no hay módulo Mod4KO conectado).

---

## Ciclo Principal (Main Loop)

```
main.py: BlackBoxK.__init__()
    ↓
1. AppController (inicializa modelos + controladores)
2. MainWindow + páginas (crea UI)
3. Vincular eventos (toques/swipes)
4. _schedule_sensor_read() - Inicia timer periódico
5. _schedule_relay_eval() - Inicia timer periódico
    ↓
window.run() → Tkinter mainloop inicia
    ↓
[CADA 500ms SENSOR]:
    SensorController.read_all_sensors()
        → HardwareManager.read_analog_channel(0-7)
        → converters.adc_to_uservalue()
        → SensorData.update()
    _update_sensor_ui()
        → pressure_cards[i].update_value()
        → temp_cards[i].update_value()
    schedule siguiente lectura
    ↓
[CADA 500ms RELÉS]:
    RelayController.evaluate_and_write()
        → compara valores con setpoints
        → genera byte de estado
        → HardwareManager.write_relay_state()
    _update_relay_ui()
        → relay_indicators[i].set_active/inactive()
    schedule siguiente evaluación
    ↓
[CUANDO USUARIO TOCA PANTALLA]:
    _on_touch_start() → inicia timer para config
    _on_touch_end()
        → interpreta swipe
        → NavigationController.on_swipe_left/right()
        → MainWindow.navigate_to_page()
    Si toca 15 segundos → _open_config_menu()
```

---

## Capa MODELS - Datos y Estado

### ConfigManager (`models/config_manager.py`)

**Responsabilidad:** Cargar, validar y guardar `relay_config.json`.

**Métodos importantes:**
- `load_config()` - Carga JSON del disco
- `save_config()` - Guarda configuración actual
- `get_inputs() / get_relays()` - Obtiene diccionarios
- `update_input() / update_relay()` - Modifica y guarda

**Ejemplo de uso:**
```python
config = ConfigManager()
relay_cfg = config.get_relay("relay1")
print(relay_cfg["setpoint"])  # → 25.0
```

---

### SensorData (`models/sensor_data.py`)

**Responsabilidad:** Almacenar estado actual de sensores (thread-safe con Lock).

**Métodos importantes:**
- `update(key, value)` - Actualiza un sensor
- `get(key)` - Obtiene valor actual
- `get_all()` - Snapshot de todos
- `get_pressures() / get_temperatures()` - Filtrados

**Ejemplo de uso:**
```python
sensor_data = SensorData()
sensor_data.update("P1", 23.5)
print(sensor_data.get("P1"))  # → 23.5
```

---

### HardwareManager (`models/hardware_manager.py`)

**Responsabilidad:** Interfaz con hardware SPI (real o simulado).

**Modos de operación:**
- **Raspberry Pi con hardware real**: Comunica con Módulo Mod8AI/Mod4KO vía SPI usando `widgetlords`
- **Windows / Simulación**: Genera valores ficticios (sensores aleatorios, relés virtuales, logs de estado)

El modo se detecta automáticamente:
- Si importar `widgetlords` falla → modo SIMULACIÓN
- Si importar `widgetlords` ok y está en Raspberry Pi → modo REAL

**Métodos importantes:**
- `read_analog_channel(channel: int) -> int` - Lee ADC valor 0-4095 (simulado o real)
- `write_relay_state(byte: int)` - Escribe estado de 4 relés (b0-b3)
- `is_simulation() -> bool` - Retorna True si está en modo SIMULACIÓN

**Ejemplo de uso (automático en AppController):**
```python
hw = HardwareManager()  # Detecta automáticamente modo
if hw.is_simulation():
    print("Modo SIMULACIÓN - desarrollo en Windows")
else:
    print("Modo REAL - hardware Raspberry Pi")

value = hw.read_analog_channel(0)  # 0-4095
hw.write_relay_state(0b0101)  # Activa relés 0 y 2
```

---

## Capa CONTROLLERS - Lógica de Negocio

### AppController (`controllers/app_controller.py`)

**Responsabilidad:** Orquestación principal. Coordina modelos y proporciona interfaz unificada.

**Métodos principales:**
- `read_sensors()` - Lee todos los sensores
- `evaluate_relays()` - Evalúa lógica de relés
- `get_sensor_value(key)` - Obtiene valor de un sensor
- `update_input_config()` / `update_relay_config()` - Modifica config

**Flujo titiritero:**
```
En main.py:
    app = AppController()
    app.read_sensors()
    sensor_value = app.get_sensor_value("P1")
```

---

### SensorController (`controllers/sensor_controller.py`)

**Responsabilidad:** Lee hardware y convierte 4-20mA a unidades de usuario.

**Flujo:**
1. Leer ADC del hardware → `HardwareManager.read_analog_channel()`
2. Convertir ADC a mA → `converters.adc_to_milliamps()`
3. Convertir mA a unidades usuario → `converters.milliamps_to_uservalue()`
4. Actualizar estado → `SensorData.update()`

**Ejemplo:**
```python
# Canal 0 (P1) lee ADC=2500
# Config: min=0 PSI, max=232 PSI
# Resultado: P1 = 145.3 PSI
```

---

### RelayController (`controllers/relay_controller.py`)

**Responsabilidad:** Evalúa lógica de activación de relés.

**Lógica:**
```python
for i in range(4):
    sensor_value = sensor_data.get(relay_config[channel])
    setpoint = relay_config[setpoint]
    
    if "Max" in relay_config[function]:
        active = sensor_value >= setpoint
    elif "Min" in relay_config[function]:
        active = sensor_value <= setpoint
    
    if active:
        relay_state |= (1 << i)

hardware_manager.write_relay_state(relay_state)
```

---

### NavigationController (`controllers/navigation.py`)

**Responsabilidad:** Interpreta gestos y navega entre páginas.

**Métodos:**
- `on_splash_touched()` - Splash → Página 1
- `on_swipe_left()` - Siguiente página
- `on_swipe_right()` - Página anterior
- `go_to_page(num)` - Ir a página específica

---

## Capa VIEWS - Interfaz de Usuario

### MainWindow (`views/main_window.py`)

**Responsabilidad:** Ventana raíz y canvas principal.

**Características:**
- Canvas desplazable horizontalmente
- Contiene 4 frames (pages) yuxtapuestos
- Método `navigate_to_page()` para smooth scroll

**Código en main.py:**
```python
window = MainWindow()
window.add_frame("splash", splash_frame, 0)
window.navigate_to_page(1)  # Va a página 1
```

---

### Páginas (`views/splash_page.py`, `views/sensor_page.py`, `views/relay_page.py`)

Cada página es un `tk.Frame` que contiene:
- **Splash:** Texto de bienvenida
- **Sensor:** 4 tarjetas con valores (SensorCard)
- **Relay:** 4 indicadores de estado (RelayIndicator)

**Actualización desde controlador:**
```python
# En main.py → _update_sensor_ui()
pressure_cards[0].update_value("23.5")
relay_indicators[0].set_active("Relay 1")
```

---

### Diálogos (`views/config_dialogs.py`)

Funciones que crean ventanas de diálogo:
- `show_input_config_dialog()` - Editar sensor
- `show_relay_config_dialog()` - Editar relé
- `show_config_menu()` - Menú principal

**Callback al guardar:**
```python
def on_save(name, min_val, max_val):
    app.update_input_config(key, name, min_val, max_val)
```

---

## Capa UTILS - Herramientas

### constants.py
Centraliza todas las constantes: colores, tamaños, defaults, etc.

```python
COLOR_PRIMARY = "#007acc"
WINDOW_WIDTH = 800
DEFAULT_CONFIG = { ... }
```

### logger.py
Sistema de logging singleton con niveles (debug, info, warning, error).

```python
from utils.logger import get_logger
logger = get_logger()
logger.info("ComponentName", "Mensaje aquí")
```

### converters.py
Funciones de conversión 4-20mA.

```python
adc_val = 2500
ma = adc_to_milliamps(adc_val)      # → 12.5 mA
user_val = milliamps_to_uservalue(ma, 0, 232)  # → 145.3 PSI
```

---

## Cómo Seguir el Flujo del Código

### Pregunta: "¿Qué pasa cuando leo un sensor?"

1. **Cada 500ms:** `BlackBoxK._schedule_sensor_read()` llama `app.read_sensors()`
2. `AppController.read_sensors()` → `SensorController.read_all_sensors()`
3. Por cada sensor:
   - `HardwareManager.read_analog_channel(channel)` lee ADC
   - `converters.adc_to_uservalue()` convierte
   - `SensorData.update(key, value)` guarda estado
4. `BlackBoxK._update_sensor_ui()` actualiza `pressure_cards[i].update_value()`
5. Tkinter renderiza cambio en pantalla

### Pregunta: "¿Qué pasa cuando cambio un setpoint?"

1. Usuario toca esquina inferior derecha 15 segundos
2. `BlackBoxK._on_touch_end()` detecta hold
3. `_open_config_menu()` muestra diálogo
4. Usuario edita "Relay 1" setpoint de 25 a 30
5. `_open_relay_config_dialog()` llama callback `on_save()`
6. `app.update_relay_config()` → `ConfigManager.update_relay()`
7. Se guarda a `relay_config.json`
8. Próximo ciclo: `RelayController.evaluate_and_write()` usa nuevo setpoint

---

## Debug y Logging

Todos los módulos registran eventos importantes:

```bash
# Ver log en consola
python main.py

# Ver archivo de log
cat blackbox.log
```

**Niveles de log:**
- `DEBUG`: Detalles internos (valores de sensores)
- `INFO`: Eventos importantes (página cambiada, config guardada)
- `WARNING`: Situaciones inesperadas
- `ERROR`: Fallos recuperables
- `CRITICAL`: Fallos irrecuperables

**Ejemplo de log:**
```
[2026-03-21 14:32:15] [INFO] [BlackBoxK] Aplicación inicializada correctamente
[2026-03-21 14:32:16] [DEBUG] [SensorData] P1 = 23.5
[2026-03-21 14:32:16] [DEBUG] [HardwareManager] Relés escritos: 0x05
[2026-03-21 14:32:31] [INFO] [BlackBoxK] Splash tocado → Página 1
[2026-03-21 14:32:45] [INFO] [ConfigManager] Input P1 actualizado
```

---

## Extensiones Futuras

### Agregar nuevo tipo de lógica de relé

1. En `utils/constants.py`, agregar función:
   ```python
   RELAY_FUNCTIONS = [
       ...
       "Pressure Hysteresis"  # Nueva
   ]
   ```

2. En `controllers/relay_controller.py`, agregar lógica:
   ```python
   if "Hysteresis" in function:
       # Tu lógica aquí
   ```

### Agregar nuevos sensores

1. En `utils/constants.py`:
   ```python
   PRESSURE_KEYS = ["P1", "P2", "P3", "P4", "P5"]  # +P5
   ```

2. Hardware automaticamente soporta canales 0-7, así que solo agregar config.

### Agregar persistencia de datos históricos

1. Crear `models/history_manager.py`
2. En `SensorController`, registrar valores con timestamp
3. Agregar página de gráficos en `views/history_page.py`

---

## Resumen

```
USER INPUT            SENSORES
    ↓                    ↓
views/             controllers/
    ↓                    ↓
EVENTOS         LÓGICA DE NEGOCIO
    ↓                    ↓
main.py ←→ app_controller.py ←→ models/
    ↓                    ↓
UI ACTUALIZADA    DATOS PERSISTIDOS
```

El código es **modular, legible y fácil de mantener** porque cada capa tiene una responsabilidad clara.

¡Ahora puedes entender qué ocurre en cada parte! 🚀

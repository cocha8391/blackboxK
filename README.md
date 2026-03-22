# Black Box K Dashboard

Un dashboard interactivo para monitoreo de presión, temperatura y control de relés en **Raspberry Pi** (y Windows). Interfaz operada por pantalla táctil que proporciona visualización en tiempo real y control automático de actuadores basado en setpoints configurables.

**Nueva arquitectura MVC**: Código modular, fácil de entender y mantener. Ver [ARCHITECTURE.md](ARCHITECTURE.md) para detalles técnicos.

---

## 📋 Requisitos del Sistema

### Hardware
- **Raspberry Pi 3** o superior (4, 4B, o 5)
- **Módulo Mod8AI** (CAN/SPI 8-channel Analog Input) en chip select CE0
- **Módulo Mod4KO** (4-channel Relay Output) en chip select CE1
- **Interfaz SPI habilitada** en Raspberry Pi
- *(Opcional)* Pantalla táctil de 7" con resolución 800x480
- *(Opcional)* Sensores 4-20mA para entrada analógica

### Software
- **Raspberry Pi OS** (Bullseye, Bookworm o similar)
- **Python 3.7** o superior
- **uv** (Package manager moderno)
- **Git** (para clonar el repositorio)

---

## 🚀 Instalación Rápida

### 1. Actualizar el Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Dependencias del Sistema
```bash
sudo apt install -y python3 python3-pip python3-tk git
```

### 3. Instalar `uv`
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

O si prefieres usar pip:
```bash
pip3 install uv
```

Verifica la instalación:
```bash
uv --version
```

### 4. Clonar el Repositorio
```bash
git clone https://github.com/sielectra/blackbox-k.git
cd blackbox-k
```

### 5. Crear Entorno Virtual con `uv`
```bash
uv venv
source .venv/bin/activate  # En systems Unix/Linux/macOS
# o en PowerShell de Windows:
# .venv\Scripts\Activate.ps1
```

### 6. Instalar Dependencias del Proyecto
```bash
uv pip install tkinter widgetlords
```

O si tienes un archivo `pyproject.toml` o `requirements.txt`:
```bash
uv pip install -r requirements.txt
```

### 7. Habilitar SPI (En Raspberry Pi)
```bash
sudo raspi-config
# Navega a: Interfacing Options → SPI → Enable
# Reinicia cuando termine
```

### 8. Configurar Permisos GPIO
```bash
sudo usermod -a -G spi,gpio $USER
# Reinicia sesión o ejecuta:
newgrp gpio
```

---

## 📖 Primeros Pasos

### Estructura del Proyecto (MVC)

```
blackbox-k/
├── main.py                  # 🎬 Inicia la aplicación aquí
├── models/                  # 📊 Datos (config, sensores, hardware)
├── controllers/             # 🧠 Lógica (lectura, evaluación, navegación)
├── views/                   # 🎨 UI (Tkinter, diálogos)
├── utils/                   # 🛠️ Utilidades (constantes, logger)
├── relay_config.json        # Config de sensores y relés (generada)
├── blackbox.log             # Log de ejecución (generada)
└── ARCHITECTURE.md          # Documentación técnica detallada
```

Para entender **qué ocurre en cada parte del código**, lee [ARCHITECTURE.md](ARCHITECTURE.md).

### Ejecutar el Dashboard
```bash
# Asegúrate de que el entorno virtual esté activado
source .venv/bin/activate

# Ejecuta el dashboard
python main.py
```

**En pantalla táctil (fullscreen):**
- El dashboard se ejecutará a pantalla completa
- Toca la pantalla de splash para comenzar
- Navega entre las 4 páginas: Presiones, Temperaturas, Relés y Configuración

**En desarrollo (sin pantalla táctil):**
```bash
python3 blackboxk_dashboard.py
# Se abrirá una ventana de 800x480 que puedes redimensionar
```

---

## ⚙️ Configuración

### Archivo `relay_config.json`

Al ejecutar por primera vez, se genera automáticamente un archivo `relay_config.json` con la configuración por defecto. Puedes modificarlo para ajustar sensores y relés.

**Estructura:**
```json
{
    "inputs": {
        "P1": {"name": "Pressure 1", "min": 0, "max": 232},
        "P2": {"name": "Pressure 2", "min": 0, "max": 232},
        "P3": {"name": "Pressure 3", "min": 0, "max": 232},
        "P4": {"name": "Pressure 4", "min": 0, "max": 232},
        "T1": {"name": "Temperature 1", "min": -10, "max": 100},
        "T2": {"name": "Temperature 2", "min": -10, "max": 100},
        "T3": {"name": "Temperature 3", "min": -10, "max": 100},
        "T4": {"name": "Temperature 4", "min": -10, "max": 100}
    },
    "relays": {
        "relay1": {"name": "Relay 1", "function": "Pressure Max", "channel": "P1", "setpoint": 0},
        "relay2": {"name": "Relay 2", "function": "Pressure Max", "channel": "P2", "setpoint": 0},
        "relay3": {"name": "Relay 3", "function": "Pressure Max", "channel": "P3", "setpoint": 0},
        "relay4": {"name": "Relay 4", "function": "Pressure Max", "channel": "P4", "setpoint": 0}
    }
}
```

**Campos configurables:**
- **Inputs (sensores):**
  - `name`: Nombre del sensor (mostrado en UI)
  - `min`: Valor mínimo de escala (para conversión 4-20mA)
  - `max`: Valor máximo de escala

- **Relays:**
  - `name`: Nombre del relé (mostrado en UI)
  - `function`: Tipo de lógica ("Pressure Max", "Pressure Min", "Temperature Max", "Temperature Min")
  - `channel`: ID del sensor que controla este relé (P1-P4, T1-T4)
  - `setpoint`: Valor umbral para activación

**Ejemplo personalizado:**
```json
{
    "inputs": {
        "P1": {"name": "Presión Bomba", "min": 0, "max": 10},
        "P2": {"name": "Presión Línea", "min": 0, "max": 5}
    },
    "relays": {
        "relay1": {"name": "Bomba Principal", "function": "Pressure Max", "channel": "P1", "setpoint": 8},
        "relay2": {"name": "Válvula Relief", "function": "Pressure Max", "channel": "P2", "setpoint": 4}
    }
}
```

---

## 🧠 Entender el Código

¿Cuáles son las **3 capas principales**? ¿Cómo **fluyen los datos**? ¿Qué ocurre cuando **lees un sensor**?

Todas las respuestas en: **➡️ [ARCHITECTURE.md](ARCHITECTURE.md)**

Este documento explica:
- Estructura MVC (Modelos, Controladores, Vistas)
- Flujo de datos (entrada → lógica → salida)
- Cada módulo y su responsabilidad
- Cómo debuggear usando logs
- Cómo agregar nuevas funcionalidades

---

## 📁 Estructura del Proyecto Detallada

```
blackbox-k/
├── main.py                     # ✅ Punto de entrada (MVC)
├── blackboxk_dashboard.py      # (DEPRECATED) Archivo original
├── relay_config.json           # Configuración (generado)
├── blackbox.log                # Log de ejecución (generado)
├── .venv/                      # Entorno virtual de Python
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
├── ARCHITECTURE.md             # Documentación técnica (¡LEE ESTO!)
│
├── models/                     # 📊 DATOS
│   ├── config_manager.py      # Gestión de relay_config.json
│   ├── sensor_data.py         # Estado de sensores
│   └── hardware_manager.py    # Interfaz SPI
│
├── controllers/                # 🧠 LÓGICA
│   ├── app_controller.py      # Orquestación
│   ├── sensor_controller.py   # Lectura sensores
│   ├── relay_controller.py    # Evaluación relés
│   └── navigation.py          # Navegación
│
├── views/                      # 🎨 INTERFAZ
│   ├── main_window.py
│   ├── splash_page.py
│   ├── sensor_page.py
│   ├── relay_page.py
│   └── config_dialogs.py
│
├── utils/                      # 🛠️ UTILIDADES
│   ├── constants.py           # Constantes
│   ├── logger.py              # Sistema de logging
│   └── converters.py          # Conversión de datos
│
└── .git/                       # Repositorio Git
```

---

## 🔧 Uso Típico

### Flujo de Operación

1. **Inicio:** El dashboard muestra splash screen "BLACK BOX K - Touch to Start"
2. **Lectura periódica (500ms):** Sensores 4-20mA se convierten a valores de usuario
3. **Evaluación de lógica:** Se evalúan setpoints de cada relé
4. **Control automático:** Se activan/desactivan relés según condiciones
5. **Visualización:** UI actualiza valores e indicadores de estado
6. **Configuración:** Puedes tocar elementos para modificar parámetros

### Navegación en UI

- **Página 1 (Splash):** Pantalla de inicio
- **Página 2 (Presiones):** Gráficas P1-P4 con valores en tiempo real
- **Página 3 (Temperaturas):** Gráficas T1-T4 con valores en tiempo real
- **Página 4 (Relés):** Estado de los 4 relés (ON/OFF)
- **Toca elementos** para acceder a configuración avanzada

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'widgetlords'"
```bash
# Asegúrate de que estés en el entorno virtual activado
source .venv/bin/activate

# Reinstala la librería
uv pip install widgetlords --force-reinstall
```

### "Error leyendo analógicos" o "Error escribiendo relés"
- **Verifica SPI habilitado:** `sudo raspi-config` → Interfacing Options → SPI → Enable
- **Verifica permisos:** `sudo usermod -a -G spi,gpio $USER`
- **Verifica conexiones:** Asegúrate de que Mod8AI esté en CE0 y Mod4KO en CE1
- **Reinicia Raspberry Pi:** `sudo reboot`

### Dashboard no aparece a pantalla completa
- En Raspberry Pi, requiere X11/Wayland. En SSH, necesitas X11 forwarding
- Ejecuta localmente en Raspberry Pi con HDMI conectado

### UI con lag o actualizaciones lentas
- Aumenta el intervalo en `root.after(500, ...)` si necesitas menos actualizaciones
- Reduce a 200-250ms si necesitas más responsividad
- Verifica carga del CPU: `top` o `htop`

### Sensores muestran valores erráticos
- Verifica calibración 4-20mA en librerías (valores 745 y 3723 en función `read_analog()`)
- Comprueba conexiones analógicas y ruido electromagnético
- Aumenta el rango min/max en configuración para estabilidad

### Relés no se activan
- Verifica logica en `"function"`: "Pressure Max", "Pressure Min", "Temperature Max", "Temperature Min"
- Comprueba `"setpoint"` está en rango válido
- Verifica canal `"channel"` existe en sensores
- Revisa salidas físicas del módulo Mod4KO

---

## 📦 Dependencias

El proyecto requiere:

- **tkinter** - GUI (incluido en Python estándar)
- **widgetlords** - Interfaz con módulos SPI Mod8AI/Mod4KO
- **Python stdlib:** json, os, copy

Para instalar todas las dependencias de una vez:
```bash
uv pip install tkinter widgetlords
```

---

## 📝 Licencia

Proyecto de SIELECTRA. Reservados todos los derechos.

---

## ✉️ Soporte

Para reportar bugs o solicitar features, contacta al equipo de desarrollo de SIELECTRA.

---

## 🔄 Versiones

| Versión | Fecha | Cambios |
|---------|-------|---------|
| 1.0 | 2026-03-21 | Versión inicial del dashboard |

---

**¡Dashboard listo para monitoreo en tiempo real! 🚀**

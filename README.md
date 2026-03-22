# Black Box K Dashboard

Un dashboard interactivo para monitoreo de presión, temperatura y control de relés. **Soporta Windows (modo simulación) y Raspberry Pi** (con hardware real). Interfaz operada por pantalla táctil que proporciona visualización en tiempo real y control automático de actuadores basado en setpoints configurables.

**Arquitectura MVC**: Código modular, mantenible y testeable. Ver [ARCHITECTURE.md](ARCHITECTURE.md) para detalles técnicos.

---

## 📋 Requisitos del Sistema

### Windows (Desarrollo y Testing)
- **Python 3.7** o superior
- **pip** (gestor de paquetes estándar)
- Ejecuta en **modo SIMULACIÓN** (sin hardware real)

### Raspberry Pi (Producción)
- **Raspberry Pi 3** o superior (4, 4B, o 5)
- **Módulo I-SPI-DIN-RTC-RS485 VPE-2701 Rev E** (8-channel Analog Input) en chip select CE0
- **Módulo PI-SPI-DIN-4KO VPE-2741 Rev B** (4-channel Relay Output) en chip select CE1
- **Interfaz SPI habilitada**
- *(Opcional)* Pantalla táctil de 7" con resolución 800x480
- *(Opcional)* Sensores 4-20mA para entrada analógica

### Software (Común)
- **Python 3.8** o superior
- **Git** (para clonar el repositorio)

---

## 🚀 Instalación Rápida

### ⚡ WINDOWS (Desarrollo)

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/sielectra/blackbox-k.git
cd blackbox-k
```

#### 2. Crear Entorno Virtual
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### 3. Instalar Dependencias
```powershell
pip install --upgrade pip
pip install pillow
```

#### 4. Ejecutar el Dashboard
```powershell
python main.py
```

✅ **La aplicación se ejecutará en modo SIMULACIÓN** (valores de sensores generados aleatoriamente, relés virtuales)

---

### 🍓 RASPBERRY PI (Producción)

#### 1. Actualizar el Sistema
```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Instalar Dependencias del Sistema
```bash
sudo apt install -y python3 python3-pip python3-tk git
```

#### 3. Clonar el Repositorio
```bash
git clone https://github.com/sielectra/blackbox-k.git
cd blackbox-k
```

#### 4. Crear Entorno Virtual
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 5. Instalar Dependencias
```bash
# Linux/Raspberry Pi
chmod +x install.sh
./install.sh

# Windows
install.bat

# O instalación manual:
pip install --upgrade pip
pip install pillow

# widgetlords NO está disponible en PyPI público
# Para instalar widgetlords, contacta al equipo de SIELECTRA
# o instala desde el repositorio interno de la empresa
```

#### 6. Habilitar SPI
```bash
sudo raspi-config
# Navega a: Interfacing Options → SPI → Enable
# Reinicia cuando termine
```

#### 7. Configurar Permisos GPIO
```bash
sudo usermod -a -G spi,gpio $USER
# Reinicia sesión o ejecuta:`
newgrp gpio
```

#### 8. Ejecutar el Dashboard
```bash
python main.py
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

#### En Windows (Modo Simulación)
```powershell
# Asegúrate de que el entorno virtual esté activado
.venv\Scripts\Activate.ps1

# Ejecuta el dashboard
python main.py
```

Una ventana de **800x480** se abrirá con valores de sensores simulados. Perfecta para **desarrollo y testing**.

#### En Raspberry Pi (Hardware Real)
```bash
# Asegúrate de que el entorno virtual esté activado
source .venv/bin/activate

# Ejecuta el dashboard
python main.py
```

Conecta una pantalla táctil de 7" (800x480) a tu Raspberry Pi:
- El dashboard se ejecutará a **pantalla completa**
- Toca la pantalla de splash para comenzar
- Navega entre las 4 páginas: Presiones, Temperaturas, Relés y Configuración
- Lee sensores 4-20mA en tiempo real
- Controla relés según setpoints configurables

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
├── install.sh                  # 🛠️ Script instalación Linux/RPi
├── install.bat                 # 🛠️ Script instalación Windows
├── WIDGETLORDS_INSTALL.md      # 📋 Instrucciones para widgetlords
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

### Windows (Modo Simulación)

#### Dashboard abre pero dice "Modo SIMULACIÓN"
✅ **Esto es correcto.** Windows no tiene hardware SPI real (Mod8AI/Mod4KO). Los sensores generan valores aleatorios para testing.

#### "ModuleNotFoundError: No module named 'widgetlords'"
✅ **Esto es normal en Windows.** No se necesita `widgetlords` (es solo para Raspberry Pi con hardware real). La aplicación automáticamente usa modo simulación.

#### La ventana no aparece
- Verifica que Python está en PATH: `python --version`
- Verifica que tkinter está instalado: `python -m tkinter` (debe abrir ventana)
- Asegúrate de activar el virtual environment: `.venv\Scripts\Activate.ps1`

#### Valores de sensores siempre iguales o no cambian
- Los valores se actualizan cada 500ms automáticamente
- Verifica que el mainloop está corriendo (ventana debe estar responsiva)

---

### Raspberry Pi (Hardware Real)

#### "ModuleNotFoundError: No module named 'widgetlords'"
`widgetlords` está disponible en el repositorio oficial **https://github.com/widgetlords**.

**Soluciones:**
1. **Instala desde el repositorio oficial:**
   ```bash
   git clone https://github.com/widgetlords/widgetlords.git
   cd widgetlords
   pip install .
   ```
2. **Instala desde releases** si hay wheels disponibles
3. **Para desarrollo/testing**, ejecuta sin `widgetlords` - la aplicación automáticamente usará **modo SIMULACIÓN**

**La aplicación funciona perfectamente en modo simulación** para desarrollo y testing sin hardware real.

📖 **Instrucciones detalladas para widgetlords**: Ver [WIDGETLORDS_INSTALL.md](WIDGETLORDS_INSTALL.md)

#### "Error leyendo analógicos" o "Error escribiendo relés"
- **Verifica SPI habilitado:** `sudo raspi-config` → Interfacing Options → SPI → Enable
- **Verifica permisos:** `sudo usermod -a -G spi,gpio $USER` y luego reinicia sesión
- **Verifica conexiones:** Asegúrate de que I-SPI-DIN-RTC-RS485 VPE-2701 esté en CE0 y PI-SPI-DIN-4KO VPE-2741 en CE1
- **Reinicia Raspberry Pi:** `sudo reboot`
- **Test SPI:** `ls /dev/spi*` debe mostrar `/dev/spidev0.0` y `/dev/spidev0.1`

#### Dashboard no aparece a pantalla completa
- En Raspberry Pi, requiere X11/Wayland. En SSH, necesitas X11 forwarding
- Ejecuta localmente en Raspberry Pi con HDMI conectado
- Verifica display: `echo $DISPLAY` (debe estar vacío o `:0`)

#### UI con lag o actualizaciones lentas
- Aumenta el intervalo en `root.after(500, ...)` si necesitas menos actualizaciones
- Reduce a 200-250ms si necesitas más responsividad
- Verifica carga del CPU: `top` o `htop`
- Verifica si hay procesos de background usando recursos

#### Sensores muestran valores erráticos
- Verifica calibración 4-20mA en converters (valores 745 y 3723 para conversión)
- Comprueba conexiones analógicas y ruido electromagnético
- Aumenta el rango min/max en configuración para estabilidad
- Verifica que sensores tengan 4-20mA correctamente alimentados

#### Relés no se activan
- Verifica lógica en `"function"`: "Pressure Max", "Pressure Min", "Temperature Max", "Temperature Min"
- Comprueba `"setpoint"` está en rango válido (entre min/max del sensor)
- Verifica canal `"channel"` existe en sensores configurados
- Revisa salidas físicas del módulo PI-SPI-DIN-4KO VPE-2741 con multímetro
- Verifica que relés están alimentados correctamente

---

## 📦 Dependencias

El proyecto requiere:

- **tkinter** - GUI (incluido en Python estándar)
- **pillow** - Procesamiento de imágenes (cuando sea necesario)
- **widgetlords** - ⚠️ **Solo en Raspberry Pi** - Interfaz con módulos SPI I-SPI-DIN-RTC-RS485 VPE-2701 y PI-SPI-DIN-4KO VPE-2741 (disponible en https://github.com/widgetlords)
- **Python stdlib:** json, os, copy, logging

### Instalación de dependencias

**En Windows (desarrollo):**
```powershell
pip install pillow
```

**En Raspberry Pi (producción):**
```bash
pip install pillow
# widgetlords: Contacta al equipo de SIELECTRA para instalación
# La aplicación funciona en MODO SIMULACIÓN sin widgetlords
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

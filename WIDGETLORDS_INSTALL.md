# Instrucciones para instalar widgetlords (Equipo SIELECTRA)

`widgetlords` es una librería para controlar módulos SPI en Raspberry Pi. El repositorio oficial está en **https://github.com/widgetlords**.

## Instalación desde repositorio oficial

### Opción 1: Desde Git (recomendado)
```bash
# Clona el repositorio oficial de widgetlords
git clone https://github.com/widgetlords/widgetlords.git
cd widgetlords

# Instala en el entorno virtual de BlackBox K
source ~/projects/blackboxK/.venv/bin/activate
pip install .
```

### Opción 2: Wheel pre-compilado
Si hay un wheel disponible en el repositorio:
```bash
# Descarga el wheel desde releases
wget [URL_DEL_WHEEL]
pip install widgetlords-*.whl
```

### Opción 3: Instalación directa desde URL
```bash
# Si hay un wheel hosteado
pip install https://github.com/widgetlords/widgetlords/releases/download/[VERSION]/widgetlords-[VERSION]-py3-none-any.whl
```

## Verificación de instalación
```bash
# Activa el entorno virtual
source ~/projects/blackboxK/.venv/bin/activate

# Verifica que widgetlords se puede importar
python3 -c "import widgetlords; print('✅ widgetlords instalado correctamente')"

# Ejecuta BlackBox K
python main.py
```

## Hardware Compatible

Esta instalación habilita soporte para:
- **I-SPI-DIN-RTC-RS485 VPE-2701 Rev E**: Módulo de entrada analógica 8-canales
- **PI-SPI-DIN-4KO VPE-2741 Rev B**: Módulo de salida de relés 4-canales

## Modo Simulación (sin widgetlords)
Si no puedes instalar widgetlords, la aplicación funcionará perfectamente en **modo simulación**:
- Sensores generan valores aleatorios
- Relés se registran en logs (sin hardware real)
- Ideal para desarrollo y testing

```bash
python main.py  # Funciona sin widgetlords
```
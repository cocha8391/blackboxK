#!/bin/bash
# Script para ejecutar BlackBox K Dashboard en Raspberry Pi
# Maneja automáticamente la configuración de display

echo "🚀 Ejecutando BlackBox K Dashboard..."

# Activar entorno virtual
source .venv/bin/activate

# Verificar si estamos en un entorno gráfico
if [ -z "$DISPLAY" ]; then
    echo "⚠️  No se detecta display gráfico (DISPLAY no está configurado)"
    echo ""
    echo "Opciones para ejecutar la aplicación:"
    echo ""
    echo "1. Ejecuta directamente en la consola de Raspberry Pi:"
    echo "   - Conecta un monitor/teclado a tu Raspberry Pi"
    echo "   - Abre la terminal y ejecuta: python main.py"
    echo ""
    echo "2. Usa SSH con X11 forwarding:"
    echo "   - Desde tu PC: ssh -X pi@tu-raspberry-pi"
    echo "   - En Raspberry Pi: export DISPLAY=:0 && python main.py"
    echo ""
    echo "3. Configura VNC:"
    echo "   - sudo apt install tightvncserver"
    echo "   - Configura VNC y conéctate desde tu PC"
    echo "   - Ejecuta la aplicación en la sesión VNC"
    echo ""
    echo "4. Para testing sin GUI (modo headless):"
    echo "   - python -c \"from controllers.app_controller import AppController; app = AppController(); print('✅ App inicializada correctamente')\""
    echo ""
    exit 1
fi

echo "✅ Display detectado: $DISPLAY"
echo "🎯 Iniciando aplicación..."

# Ejecutar la aplicación
python main.py
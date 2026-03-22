#!/bin/bash
# Script de instalación para BlackBox K Dashboard
# Compatible con Raspberry Pi y desarrollo sin widgetlords

echo "🚀 Instalando BlackBox K Dashboard..."

# Actualizar sistema (solo en Raspberry Pi)
if [ -f /etc/os-release ] && grep -q "raspbian\|raspberrypi" /etc/os-release; then
    echo "📦 Detectado Raspberry Pi - Actualizando sistema..."
    sudo apt update && sudo apt upgrade -y
    sudo apt install -y python3 python3-pip python3-tk git
else
    echo "💻 Detectado sistema de desarrollo (no Raspberry Pi)"
fi

# Crear entorno virtual
echo "🐍 Creando entorno virtual..."
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias básicas
echo "📚 Instalando dependencias..."
pip install --upgrade pip
pip install pillow

# Verificar instalación de widgetlords
echo "🔍 Verificando widgetlords..."
if python3 -c "import widgetlords" 2>/dev/null; then
    echo "✅ widgetlords encontrado - Modo HARDWARE REAL disponible"
else
    echo "⚠️  widgetlords NO encontrado"
    echo "   Intentando instalar desde https://github.com/widgetlords/widgetlords.git..."
    if command -v git >/dev/null 2>&1; then
        git clone https://github.com/widgetlords/widgetlords.git /tmp/widgetlords
        cd /tmp/widgetlords
        pip install .
        cd -
        if python3 -c "import widgetlords" 2>/dev/null; then
            echo "✅ widgetlords instalado exitosamente"
        else
            echo "❌ Falló la instalación de widgetlords - Se usará MODO SIMULACIÓN"
        fi
    else
        echo "❌ Git no disponible - Se usará MODO SIMULACIÓN"
    fi
fi

echo ""
echo "🎉 Instalación completada!"
echo ""
echo "Para ejecutar:"
echo "  source .venv/bin/activate"
echo "  python main.py"
echo ""
echo "La aplicación funcionará en modo simulación si no tienes widgetlords."
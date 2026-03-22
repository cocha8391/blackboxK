@echo off
REM Script de instalación para BlackBox K Dashboard (Windows)
REM Compatible con desarrollo sin widgetlords

echo 🚀 Instalando BlackBox K Dashboard...

REM Crear entorno virtual
echo 🐍 Creando entorno virtual...
python -m venv .venv
call .venv\Scripts\activate.bat

REM Instalar dependencias básicas
echo 📚 Instalando dependencias...
pip install --upgrade pip
pip install pillow

REM Verificar instalación de widgetlords
echo 🔍 Verificando widgetlords...
python -c "import widgetlords" 2>nul
if %errorlevel% equ 0 (
    echo ✅ widgetlords encontrado - Modo HARDWARE REAL disponible
) else (
    echo ⚠️  widgetlords NO encontrado - Se usará MODO SIMULACIÓN
    echo    widgetlords solo es necesario para Raspberry Pi con hardware real
)

echo.
echo 🎉 Instalación completada!
echo.
echo Para ejecutar:
echo   .venv\Scripts\activate.bat
echo   python main.py
echo.
echo La aplicación funcionará en modo simulación si no tienes widgetlords.
pause
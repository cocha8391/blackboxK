"""Script para probar que la aplicación inicia sin errores."""

from controllers.app_controller import AppController
from models.config_manager import ConfigManager

print("\n✓ Probando ConfigManager...")
config = ConfigManager()
print(f"✓ Config loadeda correctamente")
print(f"  - Inputs: {len(config.get_inputs())}")
print(f"  - Relays: {len(config.get_relays())}")

print("\n✓ Probando AppController...")
app = AppController()
print(f"✓ AppController inicializado")
print(f"  - Sensores: {app.sensor_controller}")
print(f"  - Relés: {app.relay_controller}")

print("\n✅ La aplicación está lista para ejecutarse en Windows y Raspberry Pi!")
print("\nPara ejecutar: python main.py")

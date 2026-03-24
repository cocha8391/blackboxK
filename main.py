"""
BLACK BOX K DASHBOARD - Aplicación principal (MVC Architecture)

Punto de entrada de la aplicación.
Orquestra toda la interacción entre Modelos, Controladores y Vistas.

ARQUITECTURA MVC:
- MODELS: Datos, configuración, estado de sensores, interfaz hardware
- CONTROLLERS: Lógica de negocio (lectura sensores, evaluación relés, navegación)
- VIEWS: Interfaz de usuario (Tkinter, diálogos, eventos)

FLUJO PRINCIPAL:
1. Inicializar AppController (modelos + controladores)
2. Crear MainWindow y páginas (vistas)
3. Vincular eventos de toque (navegación)
4. Ciclos periódicos: lectura sensores + evaluación relés + actualización UI
5. Mainloop de Tkinter

USO:
    python main.py
"""

import tkinter as tk
from controllers.app_controller import AppController
from controllers.navigation import NavigationController
from views.main_window import MainWindow
from views.splash_page import create_splash_page
from views.sensor_page import create_pressure_page, create_temperature_page
from views.relay_page import create_relay_page
from views.config_pages import (
    create_config_menu_page,
    create_input_config_page,
    create_relay_config_page,
    create_connectivity_page,
    create_info_page,
    create_config_item_page,
)
from views.config_dialogs import (
    show_config_menu,
    show_input_config_dialog,
    show_relay_config_dialog,
)
from utils.constants import (
    PAGE_SPLASH,
    PAGE_PRESSURE,
    PAGE_TEMPERATURE,
    PAGE_RELAY,
    PAGE_CONFIG_MENU,
    PAGE_INPUT_CONFIG,
    PAGE_RELAY_CONFIG,
    PAGE_CONNECTIVITY,
    PAGE_INFO,
    PAGE_CONFIG_ITEM,
    SENSOR_READ_INTERVAL,
    RELAY_EVAL_INTERVAL,
    HOLD_CONFIG_TIME,
    PRESSURE_KEYS,
    TEMPERATURE_KEYS,
    NUM_RELAYS,
    RELAY_KEYS,
)
from utils.logger import get_logger

logger = get_logger()


class BlackBoxK:
    """
    Aplicación principal - orquesta modelo, controladores y vistas.
    """

    def __init__(self, use_simulation: bool = True):
        """
        Inicializa la aplicación.

        Args:
            use_simulation: Si True, simula hardware (para Windows)
        """
        logger.info("BlackBoxK", "═" * 60)
        logger.info("BlackBoxK", "   BLACK BOX K DASHBOARD - Iniciando...")
        logger.info("BlackBoxK", "═" * 60)

        # ===== MODELOS Y CONTROLADORES =====
        self.app = AppController(use_hardware_simulation=use_simulation)
        self.nav = NavigationController()

        # ===== VISTA PRINCIPAL =====
        self.window = MainWindow()

        # ===== ITEMS DE CONFIGURACIÓN ACTUAL =====
        self.current_config_type = None  # 'input' o 'relay'
        self.current_config_key = None   # key para input, index para relay

        # ===== PÁGINAS =====
        self._setup_pages()

        # ===== EVENTOS =====
        self._setup_events()

        # ===== CICLOS PERIÓDICOS =====
        self._schedule_sensor_read()
        self._schedule_relay_eval()

        logger.info("BlackBoxK", "Aplicación inicializada correctamente")

    def _setup_pages(self) -> None:
        """Crea y configura las páginas."""
        logger.info("BlackBoxK", "Configurando páginas...")

        # Página 0: Splash
        splash_frame = create_splash_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
        )
        self.window.add_frame("splash", splash_frame, PAGE_SPLASH)

        # Página 1: Presión
        pressure_frame, self.pressure_cards = create_pressure_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
        )
        self.window.add_frame("pressure", pressure_frame, PAGE_PRESSURE)

        # Página 2: Temperatura
        temperature_frame, self.temp_cards = create_temperature_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
        )
        self.window.add_frame("temperature", temperature_frame, PAGE_TEMPERATURE)

        # Página 3: Relés
        relay_frame, self.relay_indicators = create_relay_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
        )
        self.window.add_frame("relay", relay_frame, PAGE_RELAY)

        # Página 4: Menú de configuración
        config_menu_frame = create_config_menu_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
            self._on_input_config,
            self._on_relay_config,
            self._on_connectivity,
            self._on_info,
            self._on_config_close,
        )
        self.window.add_frame("config_menu", config_menu_frame, PAGE_CONFIG_MENU)

        # Página 5: Configuración de inputs
        input_config_frame = create_input_config_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
            self.app,
            self._on_select_input,
            self._on_back_to_config_menu,
        )
        self.window.add_frame("input_config", input_config_frame, PAGE_INPUT_CONFIG)

        # Página 6: Configuración de relés
        relay_config_frame = create_relay_config_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
            self.app,
            self._on_select_relay,
            self._on_back_to_config_menu,
        )
        self.window.add_frame("relay_config", relay_config_frame, PAGE_RELAY_CONFIG)

        # Página 7: Conectividad
        connectivity_frame = create_connectivity_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
            self._on_back_to_config_menu,
        )
        self.window.add_frame("connectivity", connectivity_frame, PAGE_CONNECTIVITY)

        # Página 8: Información
        info_frame = create_info_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
            self._on_back_to_config_menu,
        )
        self.window.add_frame("info", info_frame, PAGE_INFO)

        # Página 9: Configuración de item específico
        config_item_frame = create_config_item_page(
            self.window.container,
            self.window.page_width,
            self.window.page_height,
            self,
            self._on_save_config_item,
            self._on_back_to_config_menu,
        )
        self.window.add_frame("config_item", config_item_frame, PAGE_CONFIG_ITEM)

        logger.debug("BlackBoxK", "Páginas configuradas")

    def _setup_events(self) -> None:
        """Configura eventos de entrada (toques/swipes)."""
        self.window.bind_event("<ButtonPress-1>", self._on_touch_start)
        self.window.bind_event("<ButtonRelease-1>", self._on_touch_end)

        self.touch_start_x = 0
        self.hold_timer = None

        logger.debug("BlackBoxK", "Eventos configurados")

    def _on_touch_start(self, event) -> None:
        """Maneja presión de pantalla."""
        self.touch_start_x = event.x_root

        # Si toca esquina inferior derecha, inicia timer para configuración
        if (
            event.x > (self.window.page_width * 0.88)
            and event.y > (self.window.page_height * 0.79)
        ):
            self.hold_timer = self.window.after(
                HOLD_CONFIG_TIME, self._open_config_menu
            )

    def _on_input_config(self):
        """Navega a configuración de inputs."""
        self.window.navigate_to_page(PAGE_INPUT_CONFIG)

    def _on_relay_config(self):
        """Navega a configuración de relés."""
        self.window.navigate_to_page(PAGE_RELAY_CONFIG)

    def _on_connectivity(self):
        """Navega a conectividad."""
        self.window.navigate_to_page(PAGE_CONNECTIVITY)

    def _on_info(self):
        """Navega a información."""
        self.window.navigate_to_page(PAGE_INFO)

    def _on_config_close(self):
        """Cierra el menú de configuración (vuelve a relay page)."""
        self.window.navigate_to_page(PAGE_RELAY)

    def _on_select_input(self, config_type, key):
        """Selecciona input para configurar."""
        self.current_config_type = config_type
        self.current_config_key = key
        self.window.navigate_to_page(PAGE_CONFIG_ITEM)

    def _on_select_relay(self, config_type, index):
        """Selecciona relay para configurar."""
        self.current_config_type = config_type
        self.current_config_key = index
        self.window.navigate_to_page(PAGE_CONFIG_ITEM)

    def _on_save_config_item(self, name, min_val, max_val, function, channel, setpoint):
        """Guarda la configuración del item."""
        if self.current_config_type == 'input':
            min_val = float(min_val) if min_val else 0
            max_val = float(max_val) if max_val else 100
            self.app.update_input_config(self.current_config_key, name, min_val, max_val)
            logger.info("BlackBoxK", f"Input {self.current_config_key} actualizado")
        elif self.current_config_type == 'relay':
            relay_key = RELAY_KEYS[self.current_config_key]
            setpoint = float(setpoint) if setpoint else 0
            self.app.update_relay_config(relay_key, name, function, channel, setpoint)
            logger.info("BlackBoxK", f"Relay {relay_key} actualizado")
        # Volver al menú
        self.window.navigate_to_page(PAGE_CONFIG_MENU)

    def _on_back_to_config_menu(self):
        """Vuelve al menú de configuración."""
        self.window.navigate_to_page(PAGE_CONFIG_MENU)

    def _on_touch_end(self, event) -> None:
        """Maneja liberación de pantalla."""
        # Cancelar timer si estaba activo
        if self.hold_timer:
            self.window.root.after_cancel(self.hold_timer)
            self.hold_timer = None

        delta = event.x_root - self.touch_start_x

        # Página splash: cualquier toque va a página 1
        if self.nav.get_current_page() == PAGE_SPLASH:
            self.nav.on_splash_touched()
            self.window.navigate_to_page(self.nav.get_current_page())
            logger.info("BlackBoxK", "Splash tocado → Página 1")
            return

        # Swipe izquierda: siguiente página
        if delta < -80:
            if self.nav.on_swipe_left():
                self.window.navigate_to_page(self.nav.get_current_page())

        # Swipe derecha: página anterior
        elif delta > 80:
            if self.nav.on_swipe_right():
                self.window.navigate_to_page(self.nav.get_current_page())

    def _open_config_menu(self) -> None:
        """Abre el menú de configuración."""
        logger.info("BlackBoxK", "Abriendo menú de configuración")
        self.window.navigate_to_page(PAGE_CONFIG_MENU)

    def _show_input_selection_dialog(self) -> None:
        """Muestra diálogo para seleccionar qué input configurar."""
        dialog = tk.Toplevel(self.window.root)
        dialog.geometry("600x400")
        dialog.configure(bg="#f5f5f5")
        dialog.title("Select Input to Configure")

        tk.Label(
            dialog,
            text="Select Input",
            font=("Helvetica", 18, "bold"),
            bg="#f5f5f5",
        ).pack(pady=20)

        frame = tk.Frame(dialog, bg="#f5f5f5")
        frame.pack(pady=20)

        for key in PRESSURE_KEYS + TEMPERATURE_KEYS:
            cfg = self.app.config.get_input(key)
            name = cfg.get("name", key)

            tk.Button(
                frame,
                text=f"{key} - {name}",
                font=("Helvetica", 12),
                width=35,
                command=lambda k=key: [
                    dialog.destroy(),
                    self._open_input_config_dialog(k),
                ],
            ).pack(pady=5)

    def _open_input_config_dialog(self, key: str) -> None:
        """Abre diálogo para configurar un input específico."""
        cfg = self.app.config.get_input(key)
        current_name = cfg.get("name", key)
        current_min = cfg.get("min", 0)
        current_max = cfg.get("max", 100)

        def on_save(name, min_val, max_val):
            self.app.update_input_config(key, name, min_val, max_val)
            logger.info("BlackBoxK", f"Input {key} actualizado")

        show_input_config_dialog(
            self.window.root,
            key,
            current_name,
            current_min,
            current_max,
            on_save,
        )

    def _show_relay_selection_dialog(self) -> None:
        """Muestra diálogo para seleccionar qué relé configurar."""
        dialog = tk.Toplevel(self.window.root)
        dialog.geometry("600x400")
        dialog.configure(bg="#f5f5f5")
        dialog.title("Select Relay to Configure")

        tk.Label(
            dialog,
            text="Select Relay",
            font=("Helvetica", 18, "bold"),
            bg="#f5f5f5",
        ).pack(pady=20)

        frame = tk.Frame(dialog, bg="#f5f5f5")
        frame.pack(pady=20)

        for i, relay_key in enumerate(RELAY_KEYS):
            cfg = self.app.config.get_relay(relay_key)
            name = cfg.get("name", f"Relay {i+1}")

            tk.Button(
                frame,
                text=f"Relay {i+1} - {name}",
                font=("Helvetica", 12),
                width=35,
                command=lambda idx=i: [
                    dialog.destroy(),
                    self._open_relay_config_dialog(idx),
                ],
            ).pack(pady=5)

    def _open_relay_config_dialog(self, relay_index: int) -> None:
        """Abre diálogo para configurar un relé específico."""
        relay_key = RELAY_KEYS[relay_index]
        cfg = self.app.config.get_relay(relay_key)

        current_name = cfg.get("name", f"Relay {relay_index + 1}")
        current_function = cfg.get("function", "Pressure Max")
        current_channel = cfg.get("channel", "P1")
        current_setpoint = cfg.get("setpoint", 0)

        def on_save(name, function, channel, setpoint):
            self.app.update_relay_config(
                relay_key, name, function, channel, setpoint
            )
            logger.info("BlackBoxK", f"Relay {relay_key} actualizado")

        show_relay_config_dialog(
            self.window.root,
            relay_index + 1,
            current_name,
            current_function,
            current_channel,
            current_setpoint,
            on_save,
        )

    def _schedule_sensor_read(self) -> None:
        """Programa lectura periódica de sensores."""
        self.app.read_sensors()
        self._update_sensor_ui()
        self.window.after(SENSOR_READ_INTERVAL, self._schedule_sensor_read)

    def _update_sensor_ui(self) -> None:
        """Actualiza la UI con valores de sensores."""
        # Actualizar página de presión
        for i, key in enumerate(PRESSURE_KEYS):
            value = self.app.get_sensor_value(key)
            self.pressure_cards[i].update_value(f"{value}")

        # Actualizar página de temperatura
        for i, key in enumerate(TEMPERATURE_KEYS):
            value = self.app.get_sensor_value(key)
            self.temp_cards[i].update_value(f"{value}")

    def _schedule_relay_eval(self) -> None:
        """Programa evaluación periódica de relés."""
        self.app.evaluate_relays()
        self._update_relay_ui()
        self.window.after(RELAY_EVAL_INTERVAL, self._schedule_relay_eval)

    def _update_relay_ui(self) -> None:
        """Actualiza la UI con estado de relés."""
        for i in range(NUM_RELAYS):
            relay_key = RELAY_KEYS[i]
            cfg = self.app.config.get_relay(relay_key)
            relay_name = cfg.get("name", f"Relay {i+1}")

            is_active = self.app.is_relay_active(i)

            if is_active:
                self.relay_indicators[i].set_active(relay_name)
            else:
                self.relay_indicators[i].set_inactive(relay_name)

    def run(self) -> None:
        """Inicia la aplicación (bloquea hasta cerrar)."""
        logger.info("BlackBoxK", "Iniciando mainloop...")
        self.window.run()

    def shutdown(self) -> None:
        """Limpia recursos y cierra la aplicación."""
        logger.info("BlackBoxK", "Cerrando aplicación...")
        self.app.shutdown()


def main():
    """Punto de entrada principal."""
    try:
        # Crear y ejecutar aplicación
        # use_simulation=True para Windows, False para Raspberry Pi con hardware real
        app = BlackBoxK(use_simulation=True)
        app.run()

    except KeyboardInterrupt:
        logger.info("main", "Aplicación interrumpida por usuario")

    except Exception as e:
        logger.error("main", f"Error fatal: {e}", exception=e)

    finally:
        logger.info("main", "Aplicación terminada")


if __name__ == "__main__":
    main()

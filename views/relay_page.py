"""
Página de Relés - Indicadores de estado de relés.
"""

import tkinter as tk
from utils.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BG_PAGE,
    COLOR_BG_MAIN,
    COLOR_RELAY_ON,
    COLOR_RELAY_OFF,
    TEXT_COLOR_RELAY_ON,
    TEXT_COLOR_RELAY_OFF,
    COLOR_PRIMARY,
    NUM_RELAYS,
    RELAY_KEYS,
)


class RelayIndicator:
    """Indicador para mostrar el estado de un relé."""

    def __init__(self, parent: tk.Frame, relay_name: str, relay_index: int, on_toggle_callback=None):
        """
        Crea un indicador de relé.

        Args:
            parent: Frame padre
            relay_name: Nombre del relé
            relay_index: Índice del relé (0-3)
            on_toggle_callback: Función a llamar cuando se hace toggle manual
        """
        self.frame = tk.Frame(parent, bg=COLOR_BG_MAIN, width=500, height=70)
        self.frame.pack_propagate(False)

        self.relay_index = relay_index
        self.on_toggle_callback = on_toggle_callback
        self.is_manual = False

        self.label = tk.Label(
            self.frame,
            text=f"{relay_name} OFF",
            font=("Helvetica", 18, "bold"),
            fg=TEXT_COLOR_RELAY_OFF,
            bg=COLOR_BG_MAIN,
        )
        self.label.pack(expand=True)

        # Etiqueta de modo manual
        self.manual_label = tk.Label(
            self.frame,
            text="",
            font=("Helvetica", 10),
            fg=COLOR_PRIMARY,
            bg=COLOR_BG_MAIN,
        )
        self.manual_label.pack()

        # Frame principal con binding de click
        if on_toggle_callback:
            self.frame.bind("<Button-1>", lambda e: self._on_click())
            self.label.bind("<Button-1>", lambda e: self._on_click())
            self.manual_label.bind("<Button-1>", lambda e: self._on_click())

        self._bg = COLOR_BG_MAIN

    def _on_click(self):
        """Maneja el click en el indicador."""
        if self.is_manual and self.on_toggle_callback:
            self.on_toggle_callback(self.relay_index)

    def set_manual_mode(self, is_manual: bool):
        """Configura si el relé está en modo manual."""
        self.is_manual = is_manual
        if is_manual:
            self.manual_label.config(text="(Manual - Touch to toggle)")
        else:
            self.manual_label.config(text="")

    def set_active(self, relay_name: str) -> None:
        """Marca el relé como activo."""
        self.label.config(
            text=f"{relay_name} ON",
            fg=TEXT_COLOR_RELAY_ON,
        )
        self.frame.config(bg=COLOR_RELAY_ON)
        self._bg = COLOR_RELAY_ON

    def set_inactive(self, relay_name: str) -> None:
        """Marca el relé como inactivo."""
        self.label.config(
            text=f"{relay_name} OFF",
            fg=TEXT_COLOR_RELAY_OFF,
        )
        self.frame.config(bg=COLOR_RELAY_OFF)
        self._bg = COLOR_RELAY_OFF

    def place(self, **kwargs) -> None:
        """Posiciona el indicador."""
        self.frame.place(**kwargs)


def create_relay_page(container: tk.Canvas, width: int, height: int, app_controller, on_toggle_callback=None) -> tuple:
    """
    Crea la página de relés.

    Args:
        container: Canvas contenedor
        width: Ancho de la página
        height: Alto de la página
        app_controller: Controlador de la aplicación
        on_toggle_callback: Función callback para toggle manual (opcional)

    Returns:
        tuple: (frame, lista_de_indicadores)
    """
    frame = tk.Frame(container, width=width, height=height, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título
    tk.Label(
        frame,
        text="RELAYS",
        font=("Helvetica", 20, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    ).pack(pady=10)

    # Función de callback para toggle manual (usar el proporcionado o uno por defecto)
    if on_toggle_callback is None:
        def on_relay_toggle(relay_index):
            app_controller.relay_controller.toggle_manual_relay(relay_index)
        toggle_callback = on_relay_toggle
    else:
        toggle_callback = on_toggle_callback

    # Crear indicadores
    indicators = []
    for i in range(NUM_RELAYS):
        relay_key = RELAY_KEYS[i]
        cfg = app_controller.config.get_relay(relay_key)
        relay_name = cfg.get("name", f"Relay {i+1}")
        
        indicator = RelayIndicator(frame, relay_name, i, toggle_callback)
        
        # Verificar si está en modo manual
        is_manual = app_controller.relay_controller.is_relay_manual(i)
        indicator.set_manual_mode(is_manual)
        
        indicator.place(
            relx=0.5,
            rely=0.2 + i * 0.15,
            anchor="center",
        )
        indicators.append(indicator)

    return frame, indicators

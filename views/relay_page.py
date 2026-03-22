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
)


class RelayIndicator:
    """Indicador para mostrar el estado de un relé."""

    def __init__(self, parent: tk.Frame, relay_name: str):
        """
        Crea un indicador de relé.

        Args:
            parent: Frame padre
            relay_name: Nombre del relé
        """
        self.frame = tk.Frame(parent, bg=COLOR_BG_MAIN, width=500, height=70)
        self.frame.pack_propagate(False)

        self.label = tk.Label(
            self.frame,
            text=f"{relay_name} OFF",
            font=("Helvetica", 18, "bold"),
            fg=TEXT_COLOR_RELAY_OFF,
            bg=COLOR_BG_MAIN,
        )
        self.label.pack(expand=True)

        self._bg = COLOR_BG_MAIN

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


def create_relay_page(container: tk.Canvas) -> tuple:
    """
    Crea la página de relés.

    Args:
        container: Canvas contenedor

    Returns:
        tuple: (frame, lista_de_indicadores)
    """
    frame = tk.Frame(container, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título
    tk.Label(
        frame,
        text="RELAYS",
        font=("Helvetica", 20, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    ).pack(pady=10)

    # Crear indicadores
    indicators = []
    for i in range(NUM_RELAYS):
        indicator = RelayIndicator(frame, f"Relay {i+1}")
        indicator.place(
            relx=0.5,
            rely=0.2 + i * 0.15,
            anchor="center",
        )
        indicators.append(indicator)

    return frame, indicators

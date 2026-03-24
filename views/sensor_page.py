"""
Páginas de sensores - Presión y Temperatura.
"""

import tkinter as tk
from utils.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BG_PAGE,
    COLOR_BG_MAIN,
    COLOR_PRIMARY,
    NUM_PRESSURE_SENSORS,
    NUM_TEMPERATURE_SENSORS,
    PRESSURE_UNIT,
    TEMPERATURE_UNIT,
)


class SensorCard:
    """Tarjeta para mostrar un valor de sensor."""

    def __init__(self, parent: tk.Frame, title: str, unit: str):
        """
        Crea una tarjeta de sensor.

        Args:
            parent: Frame padre
            title: Nombre del sensor
            unit: Unidad (PSI, °C, etc)
        """
        self.frame = tk.Frame(parent, bg=COLOR_BG_MAIN, width=300, height=160)
        self.frame.pack_propagate(False)

        # Etiqueta de título
        self.title_label = tk.Label(
            self.frame,
            text=title,
            font=("Helvetica", 14, "bold"),
            bg=COLOR_BG_MAIN,
        )
        self.title_label.pack(pady=10)

        # Valor numérico
        self.value_label = tk.Label(
            self.frame,
            text="0",
            font=("Helvetica", 32, "bold"),
            fg=COLOR_PRIMARY,
            bg=COLOR_BG_MAIN,
        )
        self.value_label.pack()

        # Unidad
        tk.Label(self.frame, text=unit, bg=COLOR_BG_MAIN).pack()

    def update_title(self, title: str) -> None:
        """Actualiza el título de la tarjeta."""
        self.title_label.config(text=title)

    def update_value(self, value: str) -> None:
        """Actualiza el valor mostrado."""
        self.value_label.config(text=value)

    def place(self, **kwargs) -> None:
        """Posiciona la tarjeta."""
        self.frame.place(**kwargs)


def create_pressure_page(container: tk.Canvas, width: int, height: int) -> tuple:
    """
    Crea la página de sensores de presión.

    Args:
        container: Canvas contenedor
        width: Ancho de la pantalla
        height: Alto de la pantalla

    Returns:
        tuple: (frame, lista_de_cards)
    """
    frame = tk.Frame(container, width=width, height=height, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título
    tk.Label(
        frame,
        text="PRESSURE",
        font=("Helvetica", 20, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    ).pack(pady=10)

    # Crear tarjetas
    cards = []
    for i in range(NUM_PRESSURE_SENSORS):
        card = SensorCard(frame, f"P{i+1}", PRESSURE_UNIT)
        card.place(
            x=70 + (i % 2) * 360,
            y=80 + (i // 2) * 210,
        )
        cards.append(card)

    return frame, cards


def create_temperature_page(container: tk.Canvas, width: int, height: int) -> tuple:
    """
    Crea la página de sensores de temperatura.

    Args:
        container: Canvas contenedor
        width: Ancho de la pantalla
        height: Alto de la pantalla

    Returns:
        tuple: (frame, lista_de_cards)
    """
    frame = tk.Frame(container, width=width, height=height, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título
    tk.Label(
        frame,
        text="TEMPERATURE",
        font=("Helvetica", 20, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    ).pack(pady=10)

    # Crear tarjetas
    cards = []
    for i in range(NUM_TEMPERATURE_SENSORS):
        card = SensorCard(frame, f"T{i+1}", TEMPERATURE_UNIT)
        card.place(
            x=70 + (i % 2) * 360,
            y=80 + (i // 2) * 210,
        )
        cards.append(card)

    return frame, cards

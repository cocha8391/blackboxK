"""
Página Splash - Pantalla de bienvenida.
"""

import tkinter as tk
from utils.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BG_MAIN,
    COLOR_PRIMARY,
)


def create_splash_page(container: tk.Canvas) -> tk.Frame:
    """
    Crea la página splash (bienvenida).

    Args:
        container: Canvas contenedor

    Returns:
        tk.Frame: Frame de la página splash
    """
    frame = tk.Frame(container, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=COLOR_BG_MAIN)
    frame.pack_propagate(False)

    # Título principal
    tk.Label(
        frame,
        text="BLACK BOX K",
        font=("Helvetica", 32, "bold"),
        bg=COLOR_BG_MAIN,
        fg=COLOR_PRIMARY,
    ).place(relx=0.5, rely=0.4, anchor="center")

    # Subtítulo
    tk.Label(
        frame,
        text="Touch to Start",
        font=("Helvetica", 16),
        bg=COLOR_BG_MAIN,
    ).place(relx=0.5, rely=0.6, anchor="center")

    # Pie de página
    tk.Label(
        frame,
        text="By SIELECTRA",
        font=("Helvetica", 10),
        bg=COLOR_BG_MAIN,
    ).place(relx=0.5, rely=0.9, anchor="center")

    return frame

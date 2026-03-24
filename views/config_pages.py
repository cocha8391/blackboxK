"""
Páginas de configuración - Menú y subpáginas.
"""

import tkinter as tk
from utils.constants import (
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    COLOR_BG_PAGE,
    COLOR_BG_MAIN,
    COLOR_PRIMARY,
    PRESSURE_KEYS,
    TEMPERATURE_KEYS,
    RELAY_KEYS,
    NUM_RELAYS,
)


def create_config_menu_page(container: tk.Canvas, width: int, height: int, on_input_config, on_relay_config, on_connectivity, on_info, on_close) -> tk.Frame:
    """
    Crea la página de menú de configuración.

    Args:
        container: Canvas contenedor
        width: Ancho de la página
        height: Alto de la página
        on_input_config: Callback para configurar inputs
        on_relay_config: Callback para configurar relés
        on_connectivity: Callback para conectividad
        on_info: Callback para información
        on_close: Callback para cerrar

    Returns:
        tk.Frame: Frame de la página
    """
    frame = tk.Frame(container, width=width, height=height, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título
    tk.Label(
        frame,
        text="CONFIGURATION MENU",
        font=("Helvetica", 24, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    ).pack(pady=20)

    # Botones
    button_frame = tk.Frame(frame, bg=COLOR_BG_PAGE)
    button_frame.pack(pady=50)

    tk.Button(
        button_frame,
        text="Configure Inputs",
        font=("Helvetica", 16),
        width=20,
        command=on_input_config,
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="Configure Relays",
        font=("Helvetica", 16),
        width=20,
        command=on_relay_config,
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="Connectivity",
        font=("Helvetica", 16),
        width=20,
        command=on_connectivity,
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="Information",
        font=("Helvetica", 16),
        width=20,
        command=on_info,
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="Close",
        font=("Helvetica", 16),
        width=20,
        command=on_close,
    ).pack(pady=20)

    return frame


def create_input_config_page(container: tk.Canvas, width: int, height: int, app_controller, on_back) -> tk.Frame:
    """
    Crea la página de configuración de inputs.

    Args:
        container: Canvas contenedor
        width: Ancho de la página
        height: Alto de la página
        app_controller: Controlador de la app
        on_back: Callback para volver

    Returns:
        tk.Frame: Frame de la página
    """
    frame = tk.Frame(container, width=width, height=height, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título
    tk.Label(
        frame,
        text="INPUT CONFIGURATION",
        font=("Helvetica", 20, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    ).pack(pady=10)

    # Lista de inputs
    list_frame = tk.Frame(frame, bg=COLOR_BG_PAGE)
    list_frame.pack(pady=20)

    for key in PRESSURE_KEYS + TEMPERATURE_KEYS:
        cfg = app_controller.config.get_input(key)
        name = cfg.get("name", key)

        tk.Button(
            list_frame,
            text=f"{key} - {name}",
            font=("Helvetica", 12),
            width=30,
            command=lambda k=key: _open_input_config_dialog(frame, app_controller, k),
        ).pack(pady=5)

    # Botón back
    tk.Button(
        frame,
        text="Back to Menu",
        font=("Helvetica", 14),
        command=on_back,
    ).pack(pady=20)

    return frame


def create_relay_config_page(container: tk.Canvas, width: int, height: int, app_controller, on_back) -> tk.Frame:
    """
    Crea la página de configuración de relés.

    Args:
        container: Canvas contenedor
        width: Ancho de la página
        height: Alto de la página
        app_controller: Controlador de la app
        on_back: Callback para volver

    Returns:
        tk.Frame: Frame de la página
    """
    frame = tk.Frame(container, width=width, height=height, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título
    tk.Label(
        frame,
        text="RELAY CONFIGURATION",
        font=("Helvetica", 20, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    ).pack(pady=10)

    # Lista de relés
    list_frame = tk.Frame(frame, bg=COLOR_BG_PAGE)
    list_frame.pack(pady=20)

    for i, relay_key in enumerate(RELAY_KEYS):
        cfg = app_controller.config.get_relay(relay_key)
        name = cfg.get("name", f"Relay {i+1}")

        tk.Button(
            list_frame,
            text=f"Relay {i+1} - {name}",
            font=("Helvetica", 12),
            width=30,
            command=lambda idx=i: _open_relay_config_dialog(frame, app_controller, idx),
        ).pack(pady=5)

    # Botón back
    tk.Button(
        frame,
        text="Back to Menu",
        font=("Helvetica", 14),
        command=on_back,
    ).pack(pady=20)

    return frame


def create_connectivity_page(container: tk.Canvas, width: int, height: int, on_back) -> tk.Frame:
    """
    Crea la página de conectividad.

    Args:
        container: Canvas contenedor
        width: Ancho de la página
        height: Alto de la página
        on_back: Callback para volver

    Returns:
        tk.Frame: Frame de la página
    """
    frame = tk.Frame(container, width=width, height=height, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título
    tk.Label(
        frame,
        text="CONNECTIVITY",
        font=("Helvetica", 20, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    ).pack(pady=20)

    # Contenido placeholder
    tk.Label(
        frame,
        text="Connectivity settings will be here.",
        font=("Helvetica", 14),
        bg=COLOR_BG_PAGE,
    ).pack(pady=50)

    # Botón back
    tk.Button(
        frame,
        text="Back to Menu",
        font=("Helvetica", 14),
        command=on_back,
    ).pack(pady=20)

    return frame


def create_info_page(container: tk.Canvas, width: int, height: int, on_back) -> tk.Frame:
    """
    Crea la página de información.

    Args:
        container: Canvas contenedor
        width: Ancho de la página
        height: Alto de la página
        on_back: Callback para volver

    Returns:
        tk.Frame: Frame de la página
    """
    frame = tk.Frame(container, width=width, height=height, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título
    tk.Label(
        frame,
        text="INFORMATION",
        font=("Helvetica", 20, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    ).pack(pady=20)

    # Contenido
    info_text = """
    Black Box K Dashboard
    Version 1.0
    By SIELECTRA

    Hardware: Raspberry Pi with analog/digital modules
    Software: Python 3.8+, Tkinter
    """
    tk.Label(
        frame,
        text=info_text,
        font=("Helvetica", 12),
        bg=COLOR_BG_PAGE,
        justify="left",
    ).pack(pady=50)

    # Botón back
    tk.Button(
        frame,
        text="Back to Menu",
        font=("Helvetica", 14),
        command=on_back,
    ).pack(pady=20)

    return frame


def _open_input_config_dialog(parent_frame, app_controller, key):
    """Abre diálogo para configurar input (placeholder, integrar con existing)."""
    # Placeholder: por ahora, solo print
    print(f"Configure input {key}")


def _open_relay_config_dialog(parent_frame, app_controller, relay_index):
    """Abre diálogo para configurar relay (placeholder)."""
    print(f"Configure relay {relay_index}")
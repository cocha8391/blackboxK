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
    RELAY_FUNCTIONS,
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


def create_input_config_page(container: tk.Canvas, width: int, height: int, app_controller, on_select_input, on_back) -> tk.Frame:
    """
    Crea la página de configuración de inputs.

    Args:
        container: Canvas contenedor
        width: Ancho de la página
        height: Alto de la página
        app_controller: Controlador de la app
        on_select_input: Callback para seleccionar input (tipo, key)
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
            command=lambda k=key: on_select_input('input', k),
        ).pack(pady=5)

    # Botón back
    tk.Button(
        frame,
        text="Back to Menu",
        font=("Helvetica", 14),
        command=on_back,
    ).pack(pady=20)

    return frame


def create_relay_config_page(container: tk.Canvas, width: int, height: int, app_controller, on_select_relay, on_back) -> tk.Frame:
    """
    Crea la página de configuración de relés.

    Args:
        container: Canvas contenedor
        width: Ancho de la página
        height: Alto de la página
        app_controller: Controlador de la app
        on_select_relay: Callback para seleccionar relay (tipo, index)
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
            command=lambda idx=i: on_select_relay('relay', idx),
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


def create_config_item_page(container: tk.Canvas, width: int, height: int, blackboxk, on_save, on_back) -> tk.Frame:
    """
    Crea la página de configuración de un item específico (input o relay).

    Args:
        container: Canvas contenedor
        width: Ancho de la página
        height: Alto de la página
        app_controller: Controlador de la app
        on_save: Callback para guardar
        on_back: Callback para volver

    Returns:
        tk.Frame: Frame de la página
    """
    frame = tk.Frame(container, width=width, height=height, bg=COLOR_BG_PAGE)
    frame.pack_propagate(False)

    # Título (se actualizará)
    title_label = tk.Label(
        frame,
        text="CONFIGURE ITEM",
        font=("Helvetica", 20, "bold"),
        bg=COLOR_BG_PAGE,
        fg=COLOR_PRIMARY,
    )
    title_label.pack(pady=10)

    # Frame para campos
    fields_frame = tk.Frame(frame, bg=COLOR_BG_PAGE)
    fields_frame.pack(pady=20)

    # Campos comunes
    name_label = tk.Label(fields_frame, text="Name:", bg=COLOR_BG_PAGE, font=("Helvetica", 11))
    name_label.grid(row=0, column=0, sticky="e", padx=10, pady=8)
    name_entry = tk.Entry(fields_frame, width=30, font=("Helvetica", 10))
    name_entry.grid(row=0, column=1, padx=10, pady=8)

    # Campos específicos para input
    min_label = tk.Label(fields_frame, text="Min:", bg=COLOR_BG_PAGE, font=("Helvetica", 11))
    min_entry = tk.Entry(fields_frame, width=15, font=("Helvetica", 10))
    max_label = tk.Label(fields_frame, text="Max:", bg=COLOR_BG_PAGE, font=("Helvetica", 11))
    max_entry = tk.Entry(fields_frame, width=15, font=("Helvetica", 10))

    # Campos específicos para relay
    function_label = tk.Label(fields_frame, text="Function:", bg=COLOR_BG_PAGE, font=("Helvetica", 11))
    function_var = tk.StringVar()
    function_menu = tk.OptionMenu(fields_frame, function_var, *RELAY_FUNCTIONS)
    function_menu.config(font=("Helvetica", 10))
    channel_label = tk.Label(fields_frame, text="Channel:", bg=COLOR_BG_PAGE, font=("Helvetica", 11))
    channel_var = tk.StringVar()
    channel_menu = tk.OptionMenu(fields_frame, channel_var, *(PRESSURE_KEYS + TEMPERATURE_KEYS))
    channel_menu.config(font=("Helvetica", 10))
    setpoint_label = tk.Label(fields_frame, text="Setpoint:", bg=COLOR_BG_PAGE, font=("Helvetica", 11))
    setpoint_entry = tk.Entry(fields_frame, width=15, font=("Helvetica", 10))

    def update_fields():
        # Limpiar todos los campos primero
        name_entry.delete(0, tk.END)
        min_entry.delete(0, tk.END)
        max_entry.delete(0, tk.END)
        setpoint_entry.delete(0, tk.END)
        
        if blackboxk.current_config_type == 'input':
            title_label.config(text=f"Configure Input: {blackboxk.current_config_key}")
            cfg = blackboxk.app.config.get_input(blackboxk.current_config_key)
            
            # Cargar datos del input específico
            name_entry.insert(0, cfg.get("name", blackboxk.current_config_key))
            min_entry.insert(0, str(cfg.get("min", 0)))
            max_entry.insert(0, str(cfg.get("max", 100)))
            
            # Actualizar etiquetas según tipo de input
            if blackboxk.current_config_subtype == 'pressure':
                min_label.config(text="Min Pressure (PSI):")
                max_label.config(text="Max Pressure (PSI):")
            elif blackboxk.current_config_subtype == 'temperature':
                min_label.config(text="Min Temp (°C):")
                max_label.config(text="Max Temp (°C):")
            else:
                min_label.config(text="Minimum Value:")
                max_label.config(text="Maximum Value:")
            
            # Mostrar solo campos input
            min_label.grid(row=1, column=0, sticky="e", padx=10, pady=8)
            min_entry.grid(row=1, column=1, padx=10, pady=8, sticky="w")
            max_label.grid(row=2, column=0, sticky="e", padx=10, pady=8)
            max_entry.grid(row=2, column=1, padx=10, pady=8, sticky="w")
            
            # Ocultar campos relay
            function_label.grid_remove()
            function_menu.grid_remove()
            channel_label.grid_remove()
            channel_menu.grid_remove()
            setpoint_label.grid_remove()
            setpoint_entry.grid_remove()
            
        elif blackboxk.current_config_type == 'relay':
            relay_key = RELAY_KEYS[blackboxk.current_config_key]
            title_label.config(text=f"Configure Relay {blackboxk.current_config_key + 1}")
            cfg = blackboxk.app.config.get_relay(relay_key)
            
            # Cargar datos del relay específico
            name_entry.insert(0, cfg.get("name", f"Relay {blackboxk.current_config_key + 1}"))
            function_var.set(cfg.get("function", "Pressure Max"))
            channel_var.set(cfg.get("channel", "P1"))
            setpoint_entry.insert(0, str(cfg.get("setpoint", 0)))
            
            # Ocultar campos input
            min_label.grid_remove()
            min_entry.grid_remove()
            max_label.grid_remove()
            max_entry.grid_remove()
            
            # Mostrar solo campos relay
            function_label.grid(row=1, column=0, sticky="e", padx=10, pady=8)
            function_menu.grid(row=1, column=1, padx=10, pady=8, sticky="w")
            channel_label.grid(row=2, column=0, sticky="e", padx=10, pady=8)
            channel_menu.grid(row=2, column=1, padx=10, pady=8, sticky="w")
            setpoint_label.grid(row=3, column=0, sticky="e", padx=10, pady=8)
            setpoint_entry.grid(row=3, column=1, padx=10, pady=8, sticky="w")

    # Llamar update al crear
    update_fields()

    # Botones
    buttons_frame = tk.Frame(frame, bg=COLOR_BG_PAGE)
    buttons_frame.pack(pady=20)
    
    def on_save_click():
        """Callback para el botón Save que determina qué parámetros pasar."""
        if blackboxk.current_config_type == 'input':
            on_save(
                name_entry.get(),
                min_entry.get(),
                max_entry.get(),
                None,  # function
                None,  # channel
                None,  # setpoint
            )
        elif blackboxk.current_config_type == 'relay':
            on_save(
                name_entry.get(),
                None,  # min_val
                None,  # max_val
                function_var.get(),
                channel_var.get(),
                setpoint_entry.get(),
            )

    tk.Button(
        buttons_frame,
        text="Save",
        font=("Helvetica", 14),
        command=on_save_click,
    ).pack(side="left", padx=10)

    tk.Button(
        buttons_frame,
        text="Back",
        font=("Helvetica", 14),
        command=on_back,
    ).pack(side="left", padx=10)

    # Almacenar referencias para actualizar
    frame.title_label = title_label
    frame.name_entry = name_entry
    frame.min_label = min_label
    frame.min_entry = min_entry
    frame.max_label = max_label
    frame.max_entry = max_entry
    frame.function_label = function_label
    frame.function_menu = function_menu
    frame.channel_label = channel_label
    frame.channel_menu = channel_menu
    frame.setpoint_label = setpoint_label
    frame.setpoint_entry = setpoint_entry
    frame.update_fields = update_fields  # Guardar como método del frame
    frame.blackboxk = blackboxk  # Guardar referencia a blackboxk

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
    """Placeholder."""
    pass


def _open_relay_config_dialog(parent_frame, app_controller, relay_index):
    """Placeholder."""
    pass
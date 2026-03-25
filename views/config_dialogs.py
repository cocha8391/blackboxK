"""
Diálogos de configuración.
"""

import tkinter as tk
from tkinter import messagebox
from utils.constants import (
    COLOR_BG_DIALOG,
    COLOR_PRIMARY,
    COLOR_DANGER,
    COLOR_SUCCESS,
    RELAY_FUNCTIONS,
    PRESSURE_KEYS,
    TEMPERATURE_KEYS,
    NUM_RELAYS,
    RELAY_KEYS,
)


def show_virtual_keyboard(entry_widget):
    """Muestra un teclado virtual simple para el Entry dado."""
    import string
    vk_win = tk.Toplevel(entry_widget)
    vk_win.title("Teclado Virtual")
    vk_win.geometry("600x250")
    vk_win.grab_set()
    
    def insert_char(c):
        entry_widget.insert(tk.END, c)
    def backspace():
        entry_widget.delete(len(entry_widget.get())-1, tk.END)
    def close_vk():
        vk_win.destroy()

    chars = [
        list("1234567890"),
        list("qwertyuiop"),
        list("asdfghjklñ"),
        list("zxcvbnm.-_"),
    ]
    for row, row_chars in enumerate(chars):
        for col, c in enumerate(row_chars):
            b = tk.Button(vk_win, text=c, width=4, height=2, command=lambda ch=c: insert_char(ch))
            b.grid(row=row, column=col, padx=2, pady=2)
    # Espacio, borrar, ok
    tk.Button(vk_win, text="ESPACIO", width=10, height=2, command=lambda: insert_char(" ")).grid(row=4, column=0, columnspan=3, padx=2, pady=2)
    tk.Button(vk_win, text="BORRAR", width=10, height=2, command=backspace).grid(row=4, column=3, columnspan=3, padx=2, pady=2)
    tk.Button(vk_win, text="OK", width=10, height=2, command=close_vk).grid(row=4, column=6, columnspan=3, padx=2, pady=2)

def show_input_config_dialog(
    parent: tk.Tk,
    input_key: str,
    current_name: str,
    current_min: float,
    current_max: float,
    on_save_callback,
) -> None:
    """
    Abre diálogo para configurar un sensor.

    Args:
        parent: Ventana padre
        input_key: Identificador del sensor (P1, T2, etc)
        current_name: Nombre actual
        current_min: Mínimo actual
        current_max: Máximo actual
        on_save_callback: Función a llamar al guardar (name, min, max)
    """
    dialog = tk.Toplevel(parent)
    dialog.geometry("600x400")
    dialog.configure(bg=COLOR_BG_DIALOG)
    dialog.title(f"Configure {input_key}")

    # Título
    tk.Label(
        dialog,
        text=f"{input_key} Configuration",
        font=("Helvetica", 18, "bold"),
        bg=COLOR_BG_DIALOG,
    ).pack(pady=20)

    # Nombre
    tk.Label(dialog, text="Name:", bg=COLOR_BG_DIALOG).pack()
    entry_name = tk.Entry(dialog, width=30)
    entry_name.pack(pady=5)
    entry_name.insert(0, current_name)
    entry_name.bind("<FocusIn>", lambda e: show_virtual_keyboard(entry_name))
    entry_name.bind("<Button-1>", lambda e: show_virtual_keyboard(entry_name))

    # Mínimo
    tk.Label(dialog, text="Min Value:", bg=COLOR_BG_DIALOG).pack()
    entry_min = tk.Entry(dialog, width=30)
    entry_min.pack(pady=5)
    entry_min.insert(0, str(current_min))
    entry_min.bind("<FocusIn>", lambda e: show_virtual_keyboard(entry_min))
    entry_min.bind("<Button-1>", lambda e: show_virtual_keyboard(entry_min))

    # Máximo
    tk.Label(dialog, text="Max Value:", bg=COLOR_BG_DIALOG).pack()
    entry_max = tk.Entry(dialog, width=30)
    entry_max.pack(pady=5)
    entry_max.insert(0, str(current_max))
    entry_max.bind("<FocusIn>", lambda e: show_virtual_keyboard(entry_max))
    entry_max.bind("<Button-1>", lambda e: show_virtual_keyboard(entry_max))

    # Etiqueta de error
    error_label = tk.Label(dialog, text="", fg="red", bg=COLOR_BG_DIALOG)
    error_label.pack(pady=10)

    def on_save():
        try:
            name = entry_name.get().strip()
            min_val = float(entry_min.get())
            max_val = float(entry_max.get())

            if min_val >= max_val:
                error_label.config(text="Error: Min must be < Max")
                return

            on_save_callback(name, min_val, max_val)
            dialog.destroy()

        except ValueError:
            error_label.config(text="Error: Invalid values")

    tk.Button(
        dialog,
        text="SAVE",
        bg=COLOR_SUCCESS,
        fg="white",
        command=on_save,
    ).pack(pady=10)

    tk.Button(
        dialog,
        text="CANCEL",
        command=dialog.destroy,
    ).pack(pady=5)


def show_relay_config_dialog(
    parent: tk.Tk,
    relay_index: int,
    current_name: str,
    current_function: str,
    current_channel: str,
    current_setpoint: float,
    on_save_callback,
) -> None:
    """
    Abre diálogo para configurar un relé.

    Args:
        parent: Ventana padre
        relay_index: Índice del relé (1-4)
        current_name: Nombre actual
        current_function: Función actual
        current_channel: Canal actual
        current_setpoint: Setpoint actual
        on_save_callback: Función a llamar al guardar
    """
    dialog = tk.Toplevel(parent)
    dialog.geometry("600x450")
    dialog.configure(bg=COLOR_BG_DIALOG)
    dialog.title(f"Configure Relay {relay_index}")

    # Título
    tk.Label(
        dialog,
        text=f"Relay {relay_index} Configuration",
        font=("Helvetica", 18, "bold"),
        bg=COLOR_BG_DIALOG,
    ).pack(pady=20)

    # Nombre
    tk.Label(dialog, text="Name:", bg=COLOR_BG_DIALOG).pack()
    entry_name = tk.Entry(dialog, width=30)
    entry_name.pack(pady=5)
    entry_name.insert(0, current_name)
    entry_name.bind("<FocusIn>", lambda e: show_virtual_keyboard(entry_name))
    entry_name.bind("<Button-1>", lambda e: show_virtual_keyboard(entry_name))

    # Función
    tk.Label(dialog, text="Function:", bg=COLOR_BG_DIALOG).pack()
    func_var = tk.StringVar(value=current_function)
    func_menu = tk.OptionMenu(dialog, func_var, *RELAY_FUNCTIONS)
    func_menu.pack(pady=5)

    # Canal
    tk.Label(dialog, text="Channel (Sensor):", bg=COLOR_BG_DIALOG).pack()
    all_channels = PRESSURE_KEYS + TEMPERATURE_KEYS
    channel_var = tk.StringVar(value=current_channel)
    channel_menu = tk.OptionMenu(dialog, channel_var, *all_channels)
    channel_menu.pack(pady=5)

    # Setpoint
    tk.Label(dialog, text="Setpoint:", bg=COLOR_BG_DIALOG).pack()
    entry_sp = tk.Entry(dialog, width=30)
    entry_sp.pack(pady=5)
    entry_sp.insert(0, str(current_setpoint))
    entry_sp.bind("<FocusIn>", lambda e: show_virtual_keyboard(entry_sp))
    entry_sp.bind("<Button-1>", lambda e: show_virtual_keyboard(entry_sp))

    # Etiqueta de error
    error_label = tk.Label(dialog, text="", fg="red", bg=COLOR_BG_DIALOG)
    error_label.pack(pady=10)

    def on_save():
        try:
            name = entry_name.get().strip()
            function = func_var.get()
            channel = channel_var.get()
            setpoint = float(entry_sp.get())

            on_save_callback(name, function, channel, setpoint)
            dialog.destroy()

        except ValueError:
            error_label.config(text="Error: Invalid setpoint value")

    tk.Button(
        dialog,
        text="SAVE",
        bg=COLOR_SUCCESS,
        fg="white",
        command=on_save,
    ).pack(pady=10)

    tk.Button(
        dialog,
        text="CANCEL",
        command=dialog.destroy,
    ).pack(pady=5)


def show_config_menu(parent: tk.Tk, on_input_clicked, on_relay_clicked) -> None:
    """
    Abre menú de configuración principal.

    Args:
        parent: Ventana padre
        on_input_clicked: Callback cuando se hace click en "Configure Inputs"
        on_relay_clicked: Callback cuando se hace click en "Configure Relays"
    """
    config_win = tk.Toplevel(parent)
    config_win.geometry("600x400")
    config_win.configure(bg=COLOR_BG_DIALOG)
    config_win.title("Configuration Menu")

    tk.Label(
        config_win,
        text="CONFIGURATION MENU",
        font=("Helvetica", 20, "bold"),
        fg=COLOR_DANGER,
        bg=COLOR_BG_DIALOG,
    ).pack(pady=30)

    tk.Button(
        config_win,
        text="Configure Inputs",
        font=("Helvetica", 14),
        width=30,
        command=on_input_clicked,
    ).pack(pady=10)

    tk.Button(
        config_win,
        text="Configure Relays",
        font=("Helvetica", 14),
        width=30,
        command=on_relay_clicked,
    ).pack(pady=10)

    tk.Button(
        config_win,
        text="CLOSE",
        bg=COLOR_PRIMARY,
        fg="white",
        width=30,
        command=config_win.destroy,
    ).pack(pady=10)

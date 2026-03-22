import tkinter as tk
import json
import os
import copy
from widgetlords.pi_spi_din import *
from widgetlords import counts_to_value

# ---------------- CONFIG ----------------

CONFIG_FILE = "relay_config.json"

default_config = {
    "inputs": {
        "P1": {"name":"Pressure 1","min":0,"max":232},
        "P2": {"name":"Pressure 2","min":0,"max":232},
        "P3": {"name":"Pressure 3","min":0,"max":232},
        "P4": {"name":"Pressure 4","min":0,"max":232},
        "T1": {"name":"Temperature 1","min":-10,"max":100},
        "T2": {"name":"Temperature 2","min":-10,"max":100},
        "T3": {"name":"Temperature 3","min":-10,"max":100},
        "T4": {"name":"Temperature 4","min":-10,"max":100}
    },
    "relays": {
        "relay1": {"name":"Relay 1","function":"Pressure Max","channel":"P1","setpoint":0},
        "relay2": {"name":"Relay 2","function":"Pressure Max","channel":"P2","setpoint":0},
        "relay3": {"name":"Relay 3","function":"Pressure Max","channel":"P3","setpoint":0},
        "relay4": {"name":"Relay 4","function":"Pressure Max","channel":"P4","setpoint":0}
    }
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)

        # Si es versión vieja o incompleta, regenerar
        if "inputs" not in data or "relays" not in data:
            return copy.deepcopy(default_config)

        return data

    return copy.deepcopy(default_config)

def save_config():
    with open(CONFIG_FILE, "w") as f:
        json.dump(config_data, f, indent=4)

config_data = load_config()

# ---------------- HARDWARE ----------------

init()
ai_module = Mod8AI(ChipEnable.CE0)
relay_module = Mod4KO(ChipEnable.CE1)

sensor_values = {
    "P1":0,"P2":0,"P3":0,"P4":0,
    "T1":0,"T2":0,"T3":0,"T4":0
}

relay_state = 0

# ---------------- UTIL ----------------

def scale_4_20(ma, min_val, max_val):
    return ((ma - 4) / 16) * (max_val - min_val) + min_val

# ---------------- GUI ----------------

WIDTH = 800
HEIGHT = 480

root = tk.Tk()
root.attributes("-fullscreen", True)

container = tk.Canvas(root, width=WIDTH, height=HEIGHT, highlightthickness=0)
container.pack(fill="both", expand=True)
container.configure(scrollregion=(0, 0, WIDTH * 4, HEIGHT))

# Frames principales
frame_splash = tk.Frame(container, width=WIDTH, height=HEIGHT, bg="white")
frame_press = tk.Frame(container, width=WIDTH, height=HEIGHT, bg="#e9eef3")
frame_temp = tk.Frame(container, width=WIDTH, height=HEIGHT, bg="#e9eef3")
frame_relay = tk.Frame(container, width=WIDTH, height=HEIGHT, bg="#e9eef3")

container.create_window((0,0), window=frame_splash, anchor="nw")
container.create_window((WIDTH,0), window=frame_press, anchor="nw")
container.create_window((WIDTH*2,0), window=frame_temp, anchor="nw")
container.create_window((WIDTH*3,0), window=frame_relay, anchor="nw")

# ---------------- SPLASH ----------------

tk.Label(
    frame_splash,
    text="BLACK BOX K",
    font=("Helvetica", 32, "bold"),
    bg="white",
    fg="#007acc"
).place(relx=0.5, rely=0.4, anchor="center")

tk.Label(
    frame_splash,
    text="Touch to Start",
    font=("Helvetica", 16),
    bg="white"
).place(relx=0.5, rely=0.6, anchor="center")

tk.Label(
    frame_splash,
    text="By SIELECTRA",
    font=("Helvetica", 10),
    bg="white"
).place(relx=0.5, rely=0.9, anchor="center")

# ---------------- CARDS ----------------

def create_card(parent, title, unit):
    card = tk.Frame(parent, bg="white", width=300, height=160)
    card.pack_propagate(False)

    title_lbl = tk.Label(
        card,
        text=title,
        font=("Helvetica", 14, "bold"),
        bg="white"
    )
    title_lbl.pack(pady=10)

    val_lbl = tk.Label(
        card,
        text="0",
        font=("Helvetica", 32, "bold"),
        fg="#007acc",
        bg="white"
    )
    val_lbl.pack()

    unit_lbl = tk.Label(card, text=unit, bg="white")
    unit_lbl.pack()

    return card, title_lbl, val_lbl, unit_lbl

pressure_title_labels = []
pressure_value_labels = []

temp_title_labels = []
temp_value_labels = []

# Página de presión
for i in range(4):
    key = f"P{i+1}"
    name = config_data["inputs"][key]["name"]
    card, title_lbl, val_lbl, unit_lbl = create_card(frame_press, name, "PSI")
    pressure_title_labels.append(title_lbl)
    pressure_value_labels.append(val_lbl)
    card.place(x=70 + (i % 2) * 360, y=80 + (i // 2) * 210)

# Página de temperatura
for i in range(4):
    key = f"T{i+1}"
    name = config_data["inputs"][key]["name"]
    card, title_lbl, val_lbl, unit_lbl = create_card(frame_temp, name, "°C")
    temp_title_labels.append(title_lbl)
    temp_value_labels.append(val_lbl)
    card.place(x=70 + (i % 2) * 360, y=80 + (i // 2) * 210)

# ---------------- RELAY PAGE ----------------

relay_boxes = []
relay_texts = []

for i in range(4):
    box = tk.Frame(frame_relay, bg="white", width=500, height=70)
    box.place(relx=0.5, rely=0.2 + i * 0.15, anchor="center")
    box.pack_propagate(False)

    text = tk.Label(
        box,
        text=f"Relay {i+1} OFF",
        font=("Helvetica", 18, "bold"),
        fg="gray",
        bg="white"
    )
    text.pack(expand=True)

    relay_boxes.append(box)
    relay_texts.append(text)

# ---------------- REFRESH VISUALS ----------------

def refresh_input_labels():
    for i in range(4):
        p_key = f"P{i+1}"
        t_key = f"T{i+1}"
        pressure_title_labels[i].config(text=config_data["inputs"][p_key]["name"])
        temp_title_labels[i].config(text=config_data["inputs"][t_key]["name"])

def refresh_relay_labels():
    for i in range(4):
        relay_key = f"relay{i+1}"
        relay_name = config_data["relays"][relay_key]["name"]

        current_text = relay_texts[i].cget("text")
        if " ON" in current_text:
            relay_texts[i].config(text=f"{relay_name} ON")
        else:
            relay_texts[i].config(text=f"{relay_name} OFF")

# ---------------- ANALOG ----------------

def read_analog():
    try:
        # Presiones P1-P4 en canales 0-3
        for i in range(4):
            key = f"P{i+1}"
            counts = ai_module.read_single(i)
            ma = counts_to_value(counts, 745, 3723, 4, 20)

            min_val = config_data["inputs"][key]["min"]
            max_val = config_data["inputs"][key]["max"]

            value = scale_4_20(ma, min_val, max_val)
            sensor_values[key] = round(value, 1)
            pressure_value_labels[i].config(text=str(round(value, 1)))

        # Temperaturas T1-T4 en canales 4-7
        for i in range(4):
            key = f"T{i+1}"
            counts = ai_module.read_single(i + 4)
            ma = counts_to_value(counts, 745, 3723, 4, 20)

            min_val = config_data["inputs"][key]["min"]
            max_val = config_data["inputs"][key]["max"]

            value = scale_4_20(ma, min_val, max_val)
            sensor_values[key] = round(value, 1)
            temp_value_labels[i].config(text=str(round(value, 1)))

    except Exception as e:
        print("Error leyendo analógicos:", e)

    root.after(500, read_analog)

# ---------------- RELAY LOGIC ----------------

def evaluate_relays():
    global relay_state
    relay_state = 0

    for i in range(4):
        key = f"relay{i+1}"
        cfg = config_data["relays"][key]

        val = sensor_values.get(cfg["channel"], 0)
        sp = cfg["setpoint"]

        activate = False

        if "Max" in cfg["function"] and val >= sp:
            activate = True

        if "Min" in cfg["function"] and val <= sp:
            activate = True

        if activate:
            relay_state |= (1 << i)
            relay_boxes[i].config(bg="#c8f7c5")
            relay_texts[i].config(
                text=f"{cfg['name']} ON",
                fg="green",
                bg="#c8f7c5"
            )
        else:
            relay_boxes[i].config(bg="white")
            relay_texts[i].config(
                text=f"{cfg['name']} OFF",
                fg="gray",
                bg="white"
            )

    try:
        relay_module.write(relay_state)
    except Exception as e:
        print("Error escribiendo relés:", e)

    root.after(500, evaluate_relays)

# ---------------- CONFIGURATION ----------------

def open_relay_config(index):
    relay_key = f"relay{index}"
    cfg = config_data["relays"][relay_key]

    win = tk.Toplevel(root)
    win.attributes("-fullscreen", True)
    win.configure(bg="#f5f5f5")

    tk.Label(
        win,
        text=f"Relay {index} Configuration",
        font=("Helvetica", 22, "bold"),
        bg="#f5f5f5"
    ).pack(pady=30)

    tk.Label(win, text="Name", bg="#f5f5f5").pack()
    entry_name = tk.Entry(win, width=25)
    entry_name.pack()
    entry_name.insert(0, cfg["name"])

    tk.Label(win, text="Function", bg="#f5f5f5").pack()
    func_var = tk.StringVar(value=cfg["function"])
    tk.OptionMenu(
        win,
        func_var,
        "Pressure Max", "Pressure Min",
        "Temperature Max", "Temperature Min"
    ).pack()

    tk.Label(win, text="Channel", bg="#f5f5f5").pack()
    ch_var = tk.StringVar(value=cfg["channel"])
    tk.OptionMenu(
        win,
        ch_var,
        "P1", "P2", "P3", "P4",
        "T1", "T2", "T3", "T4"
    ).pack()

    tk.Label(win, text="Setpoint", bg="#f5f5f5").pack()
    entry_sp = tk.Entry(win, width=25)
    entry_sp.pack()
    entry_sp.insert(0, str(cfg["setpoint"]))

    error_lbl = tk.Label(win, text="", fg="red", bg="#f5f5f5", font=("Helvetica", 12))
    error_lbl.pack(pady=10)

    def save_changes():
        try:
            config_data["relays"][relay_key]["name"] = entry_name.get().strip()
            config_data["relays"][relay_key]["function"] = func_var.get()
            config_data["relays"][relay_key]["channel"] = ch_var.get()
            config_data["relays"][relay_key]["setpoint"] = float(entry_sp.get())

            save_config()
            refresh_relay_labels()
            win.destroy()

        except Exception as e:
            error_lbl.config(text=f"Invalid data: {e}")

    tk.Button(
        win,
        text="SAVE",
        font=("Helvetica", 14),
        bg="#007acc",
        fg="white",
        command=save_changes
    ).pack(pady=20)

    tk.Button(
        win,
        text="BACK",
        command=win.destroy
    ).pack()

def open_config():
    config_win = tk.Toplevel(root)
    config_win.geometry("800x480")
    config_win.overrideredirect(True)
    config_win.configure(bg="#f5f5f5")

    tk.Label(
        config_win,
        text="CONFIGURATION MENU",
        font=("Helvetica", 24, "bold"),
        fg="#cc0000",
        bg="#f5f5f5"
    ).pack(pady=30)

    # FRAME PARA 2 COLUMNAS
    btn_frame = tk.Frame(config_win, bg="#f5f5f5")
    btn_frame.pack(pady=20)

    buttons = [
        ("Configure Inputs", open_input_menu),
        ("Configure Relay", open_relay_menu),
        ("Conexión", open_connection_menu),
        ("Información", open_info_menu)
    ]

    for index, (text, cmd) in enumerate(buttons):
        row = index // 2
        col = index % 2

        tk.Button(
            btn_frame,
            text=text,
            font=("Helvetica", 18),
            width=25,
            height=2,
            command=cmd
        ).grid(row=row, column=col, padx=10, pady=10)

    tk.Button(
        config_win,
        text="BACK",
        font=("Helvetica", 16),
        bg="#007acc",
        fg="white",
        width=15,
        height=2,
        command=config_win.destroy
    ).place(x=600, y=400)
def open_relay_menu():
    relay_win = tk.Toplevel(root)
    relay_win.geometry("800x480")
    relay_win.overrideredirect(True)
    relay_win.configure(bg="#f5f5f5")

    tk.Label(
        relay_win,
        text="RELAY CONFIGURATION",
        font=("Helvetica", 24, "bold"),
        bg="#f5f5f5"
    ).pack(pady=30)

    btn_frame = tk.Frame(relay_win, bg="#f5f5f5")
    btn_frame.pack(pady=20)

    for i in range(4):
        tk.Button(
            btn_frame,
            text=f"Configure Relay {i+1}",
            font=("Helvetica", 18),
            width=25,
            height=2,
            command=lambda x=i+1: open_relay_config(x)
        ).pack(pady=10)

    tk.Button(
        relay_win,
        text="BACK",
        font=("Helvetica", 16),
        bg="#007acc",
        fg="white",
        width=15,
        height=2,
        command=relay_win.destroy
    ).place(x=600, y=400)


def open_connection_menu():
    connection_win = tk.Toplevel(root)
    connection_win.geometry("800x480")
    connection_win.overrideredirect(True)
    connection_win.configure(bg="#f5f5f5")

    tk.Label(
        connection_win,
        text="CONEXIÓN",
        font=("Helvetica", 24, "bold"),
        bg="#f5f5f5"
    ).pack(pady=30)

    tk.Label(
        connection_win,
        text="Pantalla reservada para configuración WiFi",
        font=("Helvetica", 16),
        bg="#f5f5f5"
    ).pack(pady=20)

    tk.Button(
        connection_win,
        text="BACK",
        font=("Helvetica", 16),
        bg="#007acc",
        fg="white",
        width=15,
        height=2,
        command=connection_win.destroy
    ).place(x=600, y=400)


def open_info_menu():
    info_win = tk.Toplevel(root)
    info_win.geometry("800x480")
    info_win.overrideredirect(True)
    info_win.configure(bg="#f5f5f5")

    tk.Label(
        info_win,
        text="INFORMACIÓN",
        font=("Helvetica", 24, "bold"),
        bg="#f5f5f5"
    ).pack(pady=30)

    tk.Label(
        info_win,
        text="Pantalla reservada para información de uso y contacto",
        font=("Helvetica", 16),
        bg="#f5f5f5"
    ).pack(pady=20)

    tk.Button(
        info_win,
        text="BACK",
        font=("Helvetica", 16),
        bg="#007acc",
        fg="white",
        width=15,
        height=2,
        command=info_win.destroy
    ).place(x=600, y=400)

def open_input_config(key):
    cfg = config_data["inputs"][key]

    win = tk.Toplevel(root)
    win.attributes("-fullscreen", True)
    win.configure(bg="#f5f5f5")

    tk.Label(
        win,
        text=f"{key} Configuration",
        font=("Helvetica", 22, "bold"),
        bg="#f5f5f5"
    ).pack(pady=30)

    tk.Label(win, text="Name", bg="#f5f5f5").pack()
    entry_name = tk.Entry(win, width=30)
    entry_name.pack()
    entry_name.insert(0, cfg["name"])

    tk.Label(win, text="Min Scale", bg="#f5f5f5").pack()
    entry_min = tk.Entry(win, width=30)
    entry_min.pack()
    entry_min.insert(0, str(cfg["min"]))

    tk.Label(win, text="Max Scale", bg="#f5f5f5").pack()
    entry_max = tk.Entry(win, width=30)
    entry_max.pack()
    entry_max.insert(0, str(cfg["max"]))

    error_lbl = tk.Label(win, text="", fg="red", bg="#f5f5f5", font=("Helvetica", 12))
    error_lbl.pack(pady=10)

def open_input_menu():
    input_win = tk.Toplevel(root)
    input_win.geometry("800x480")
    input_win.overrideredirect(True)
    input_win.configure(bg="#f5f5f5")

    tk.Label(
        input_win,
        text="INPUT CONFIGURATION",
        font=("Helvetica", 24, "bold"),
        bg="#f5f5f5"
    ).pack(pady=30)

    btn_frame = tk.Frame(input_win, bg="#f5f5f5")
    btn_frame.pack(pady=20)

    keys = list(config_data["inputs"].keys())

    for i, key in enumerate(keys):
        tk.Button(
            btn_frame,
            text=key + " - " + config_data["inputs"][key]["name"],
            font=("Helvetica", 16),
            width=30,
            command=lambda k=key: [input_win.destroy(), open_input_config(k)]
        ).grid(row=i // 2, column=i % 2, padx=10, pady=10)

    tk.Button(
        input_win,
        text="BACK",
        font=("Helvetica", 16),
        bg="#007acc",
        fg="white",
        width=15,
        height=2,
        command=input_win.destroy
    ).place(x=600, y=400)

    def save_changes():
        try:
            config_data["inputs"][key]["name"] = entry_name.get().strip()
            config_data["inputs"][key]["min"] = float(entry_min.get())
            config_data["inputs"][key]["max"] = float(entry_max.get())

            save_config()
            refresh_input_labels()
            win.destroy()

        except Exception as e:
            error_lbl.config(text=f"Invalid data: {e}")

    tk.Button(
        win,
        text="SAVE",
        font=("Helvetica", 16),
        bg="#28a745",
        fg="white",
        command=save_changes
    ).pack(pady=20)

    tk.Button(
        win,
        text="BACK",
        command=win.destroy
    ).pack()

# ---------------- NAVIGATION ----------------

current_page = 0
start_x = 0
hold_timer = None

def go(page):
    global current_page
    current_page = page
    container.xview_moveto(page / 4)

def touch_start(event):
    global start_x, hold_timer
    start_x = event.x_root

    # activar configuración si mantiene presionado esquina inferior derecha
    if event.x > WIDTH - 100 and event.y > HEIGHT - 100 and current_page != 0:
        hold_timer = root.after(15000, open_config)

def touch_end(event):
    global hold_timer, current_page

    if hold_timer:
        root.after_cancel(hold_timer)
        hold_timer = None

    delta = event.x_root - start_x

    # Splash → solo con toque simple
    if current_page == 0:
        go(1)
        return

    # Swipe izquierda
    if delta < -80 and current_page < 3:
        go(current_page + 1)

    # Swipe derecha
    elif delta > 80 and current_page > 1:
        go(current_page - 1)

# IMPORTANTE: asegurarnos que el bind esté activo
root.bind("<ButtonPress-1>", touch_start)
root.bind("<ButtonRelease-1>", touch_end)

# ---------------- START ----------------

refresh_input_labels()
refresh_relay_labels()

read_analog()
evaluate_relays()

root.mainloop()

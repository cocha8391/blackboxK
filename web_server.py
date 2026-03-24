"""
Servidor web para monitoreo en tiempo real de sensores.
Proporciona interfaz web con login y datos en tiempo real via WebSockets.
"""

import os
import threading
import time
from flask import Flask, render_template_string, request, redirect, url_for, session, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from werkzeug.security import check_password_hash, generate_password_hash

from utils.logger import get_logger

logger = get_logger()

# Configuración de usuario (hardcoded por simplicidad - en producción usar DB)
USERS = {
    "admin": generate_password_hash("admin123"),  # Usuario: admin, Contraseña: admin123
}

# Templates HTML inline
LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BlackBox K - Login</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .login-form { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        input { display: block; margin: 10px 0; padding: 10px; width: 200px; }
        button { background: #007acc; color: white; padding: 10px; border: none; cursor: pointer; width: 220px; }
        .error { color: red; }
    </style>
</head>
<body>
    <div class="login-form">
        <h2>BlackBox K Dashboard</h2>
        {% if error %}<p class="error">{{ error }}</p>{% endif %}
        <form method="post">
            <input type="text" name="username" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button type="submit">Iniciar Sesión</button>
        </form>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>BlackBox K - Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background: #f0f0f0; margin: 0; padding: 20px; }
        .header { background: #007acc; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .sensor-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; }
        .sensor-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        .sensor-value { font-size: 2em; font-weight: bold; color: #007acc; }
        .sensor-label { color: #666; margin-bottom: 10px; }
        .logout { position: absolute; top: 20px; right: 20px; }
        .logout a { color: white; text-decoration: none; }
    </style>
</head>
<body>
    <div class="header">
        <h1>BlackBox K - Monitoreo en Tiempo Real</h1>
        <div class="nav-buttons" style="margin-top:12px;">
            <a href="/dashboard" style="color:white; margin-right:8px;">Sensores</a>
            <a href="/relay" style="color:white; margin-right:8px;">Relés</a>
            <a href="/config" style="color:white; margin-right:8px;">Configuración</a>
            <a href="/history" style="color:white; margin-right:8px;">Historial CSV</a>
            <a href="/logout" style="color:white;">Cerrar Sesión</a>
        </div>
    </div>
    <div id="usb-status" style="margin:8px 0 15px 0;">USB: <strong>--</strong></div>
    <div class="sensor-grid" id="sensor-grid">
        <!-- Los sensores se cargarán dinámicamente -->
    </div>
    <div style="margin-top:20px; background:white;padding:16px; border-radius:8px; box-shadow:0 0 12px rgba(0,0,0,0.1);">
        <h2>Gráfico Histórico</h2>
        <select id="chartSensorSelect" style="margin-bottom:10px; padding:6px; font-size:14px;"></select>
        <canvas id="sensor-chart" height="200"></canvas>
    </div>

    <div id="virtual-keyboard" style="display:none;position:fixed;bottom:0;left:0;right:0;background:#f0f0f0;padding:8px;border-top:1px solid #bbb;box-shadow:0 -3px 8px rgba(0,0,0,0.2);z-index:9999;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <strong>Teclado virtual</strong>
            <button onclick="hideKeyboard()" style="padding:6px 10px;">Cerrar</button>
        </div>
        <div id="keyboard-keys" style="display:flex;flex-wrap:wrap;gap:4px;"></div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <script>
        const socket = io();
        const sensorGrid = document.getElementById('sensor-grid');

        // Crear tarjetas de sensores iniciales según configuración
        const sensors = {{ inputs | tojson }};
        Object.entries(sensors).forEach(([sensor, cfg]) => {
            const card = document.createElement('div');
            card.className = 'sensor-card';
            card.id = sensor;
            card.innerHTML = `
                <div class="sensor-label">${cfg.name || sensor}</div>
                <div class="sensor-value">--</div>
            `;
            sensorGrid.appendChild(card);
        });

        // Actualizar datos en tiempo real
        socket.on('sensor_update', function(data) {
            for (const sensor in data) {
                const card = document.getElementById(sensor);
                if (card) {
                    const valueDiv = card.querySelector('.sensor-value');
                    valueDiv.textContent = Number(data[sensor]).toFixed(1);
                }
            }
        });

        function updateUSB() {
            fetch('/export_status').then(r => r.json()).then(js => {
                document.getElementById('usb-status').innerHTML = `USB: <strong>${js.ready ? 'Conectada' : 'NO conectada'}</strong> (${js.path})`;
            });
        }

        const chartCtx = document.getElementById('sensor-chart').getContext('2d');
        const history = {};
        const maxPoints = 120;

        function buildChart(selectedSensor) {
            const labels = history[selectedSensor]?.map(item => item.t) || [];
            const data = history[selectedSensor]?.map(item => item.v) || [];
            return new Chart(chartCtx, {
                type: 'line',
                data: {
                    labels,
                    datasets: [{
                        label: selectedSensor,
                        data,
                        borderColor: 'rgba(0, 122, 204, 0.9)',
                        backgroundColor: 'rgba(0, 122, 204, 0.2)',
                        fill: true,
                        tension: 0.3,
                    }],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: { display: true, title: { display: true, text: 'Tiempo' } },
                        y: { display: true, title: { display: true, text: 'Valor' } },
                    },
                },
            });
        }

        let sensorChart = null;

        function registerSensorChart() {
            const sensorSelect = document.getElementById('chartSensorSelect');
            Object.keys(sensors).forEach(sensor => {
                const option = document.createElement('option');
                option.value = sensor;
                option.text = sensors[sensor].name || sensor;
                sensorSelect.appendChild(option);
            });
            sensorSelect.onchange = () => {
                if (sensorChart) { sensorChart.destroy(); }
                sensorChart = buildChart(sensorSelect.value);
            };

            if (sensorSelect.options.length > 0) {
                sensorSelect.selectedIndex = 0;
                sensorChart = buildChart(sensorSelect.value);
            }
        }

        setInterval(updateUSB, 3000);
        updateUSB();

        registerSensorChart();

        const keyboard = document.getElementById('virtual-keyboard');
        const keysContainer = document.getElementById('keyboard-keys');
        const characters = '1234567890qwertyuiopasdfghjklzxcvbnm@._-';

        function showKeyboard(input) {
            keyboard.style.display = 'block';
            keysContainer.innerHTML = '';
            characters.split('').forEach(ch => {
                const btn = document.createElement('button');
                btn.textContent = ch;
                btn.style.padding = '8px';
                btn.style.minWidth = '34px';
                btn.onclick = () => input.value += ch;
                keysContainer.appendChild(btn);
            });
            const backBtn = document.createElement('button');
            backBtn.textContent = 'BORRAR';
            backBtn.style.padding = '8px';
            backBtn.onclick = () => input.value = input.value.slice(0, -1);
            keysContainer.appendChild(backBtn);
            const doneBtn = document.createElement('button');
            doneBtn.textContent = 'OK';
            doneBtn.style.padding = '8px';
            doneBtn.onclick = hideKeyboard;
            keysContainer.appendChild(doneBtn);
        }

        function hideKeyboard() {
            keyboard.style.display = 'none';
        }

        document.body.addEventListener('focusin', (event) => {
            const target = event.target;
            if (target.tagName === 'INPUT') {
                showKeyboard(target);
            }
        });

        document.body.addEventListener('touchstart', () => {}, { passive: true });

        socket.on('sensor_update', function(data) {
            const selected = document.getElementById('chartSensorSelect').value;
            for (const sensor in data) {
                if (!history[sensor]) history[sensor] = [];
                history[sensor].push({ t: new Date().toLocaleTimeString(), v: Number(data[sensor]).toFixed(1) });
                if (history[sensor].length > maxPoints) history[sensor].shift();
                const card = document.getElementById(sensor);
                if (card) {
                    const valueDiv = card.querySelector('.sensor-value');
                    valueDiv.textContent = Number(data[sensor]).toFixed(1);
                }
            }
            if (sensorChart && selected) {
                const newLabels = history[selected].map(item => item.t);
                const newData = history[selected].map(item => item.v);
                sensorChart.data.labels = newLabels;
                sensorChart.data.datasets[0].data = newData;
                sensorChart.update();
            }
        });
"""


class WebServer:
    """
    Servidor web Flask con SocketIO para monitoreo en tiempo real.
    """

    def __init__(self, app_controller, host='0.0.0.0', port=5000):
        """
        Inicializa el servidor web.

        Args:
            app_controller: Controlador de la aplicación para acceder a datos
            host: Host para el servidor
            port: Puerto para el servidor
        """
        self.app_controller = app_controller
        self.host = host
        self.port = port
        self.thread = None
        self.running = False

        # Crear app Flask
        self.app = Flask(__name__)
        self.app.secret_key = 'blackbox_k_secret_key_2024'  # En producción usar variable de entorno
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        # Configurar rutas
        self._setup_routes()

        logger.info("WebServer", f"Inicializado en {host}:{port}")

    def _setup_routes(self):
        """Configura las rutas de Flask."""

        @self.app.route('/')
        def index():
            if 'username' in session:
                return redirect(url_for('dashboard'))
            return redirect(url_for('login'))

        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']

                if username in USERS and check_password_hash(USERS[username], password):
                    session['username'] = username
                    return redirect(url_for('dashboard'))
                else:
                    return render_template_string(LOGIN_TEMPLATE, error="Usuario o contraseña incorrectos")

            return render_template_string(LOGIN_TEMPLATE)

        @self.app.route('/dashboard')
        def dashboard():
            if 'username' not in session:
                return redirect(url_for('login'))
            inputs = self.app_controller.get_config().get_inputs()
            return render_template_string(DASHBOARD_TEMPLATE, inputs=inputs)

        @self.app.route('/relay')
        def relay():
            if 'username' not in session:
                return redirect(url_for('login'))
            relays = []
            for i, (key, cfg) in enumerate(self.app_controller.get_config().get_relays().items()):
                relays.append({
                    'key': key,
                    'name': cfg.get('name', key),
                    'function': cfg.get('function', ''),
                    'channel': cfg.get('channel', ''),
                    'setpoint': cfg.get('setpoint', 0),
                    'active': self.app_controller.relay_controller.is_relay_active(i),
                })
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head>
                    <title>Relés</title>
                    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
                </head>
                <body>
                <h1>Relés</h1>
                <ul id="relay-list">
                    {% for rel in relays %}
                        <li>
                            <strong>{{ rel.name }}</strong> ({{ rel.key }}) - <span id="relay-status-{{ loop.index0 }}">{{ 'ON' if rel.active else 'OFF' }}</span>
                            <button onclick="toggleRelay({{ loop.index0 }})">Toggle</button>
                        </li>
                    {% endfor %}
                </ul>
                <a href="/dashboard">Sensores</a> | <a href="/config">Configuración</a>

                <script>
                    const socket = io();
                    function toggleRelay(index) {
                        socket.emit('toggle_relay', { index });
                    }

                    socket.on('relay_update', function(data) {
                        data.active.forEach((state, i) => {
                            const el = document.getElementById('relay-status-' + i);
                            if (el) el.textContent = state ? 'ON' : 'OFF';
                        });
                    });

                    setInterval(() => socket.emit('request_status'), 2000);
                </script>
                </body>
                </html>
            ''', relays=relays)

        @self.app.route('/config')
        def config():
            if 'username' not in session:
                return redirect(url_for('login'))
            inputs = self.app_controller.get_config().get_inputs()
            relays = self.app_controller.get_config().get_relays()
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head><title>Configuración</title></head>
                <body>
                <h1>Configuración</h1>
                <h2>Entradas</h2>
                <table border="1" cellpadding="8" style="border-collapse:collapse;">
                    <tr><th>Sensor</th><th>Nombre</th><th>Min</th><th>Max</th><th>Acción</th></tr>
                    {% for key, cfg in inputs.items() %}
                    <tr>
                        <td>{{ key }}</td>
                        <td><input id="input-name-{{ key }}" value="{{ cfg.name }}"></td>
                        <td><input type="number" id="input-min-{{ key }}" value="{{ cfg.min }}"></td>
                        <td><input type="number" id="input-max-{{ key }}" value="{{ cfg.max }}"></td>
                        <td><button onclick="updateInput('{{ key }}')">Guardar</button></td>
                    </tr>
                    {% endfor %}
                </table>

                <h2>Relés</h2>
                <table border="1" cellpadding="8" style="border-collapse:collapse; margin-top:12px;">
                    <tr><th>Relé</th><th>Nombre</th><th>Función</th><th>Canal</th><th>Setpoint</th><th>Acción</th></tr>
                    {% for key, cfg in relays.items() %}
                    <tr>
                        <td>{{ key }}</td>
                        <td><input id="relay-name-{{ key }}" value="{{ cfg.name }}"></td>
                        <td><input id="relay-fn-{{ key }}" value="{{ cfg.function }}"></td>
                        <td><input id="relay-channel-{{ key }}" value="{{ cfg.channel }}"></td>
                        <td><input type="number" id="relay-setpoint-{{ key }}" value="{{ cfg.setpoint }}"></td>
                        <td><button onclick="updateRelay('{{ key }}')">Guardar</button></td>
                    </tr>
                    {% endfor %}
                </table>

                <p><a href="/dashboard">Sensores</a> | <a href="/relay">Relés</a> | <a href="/history">Historial CSV</a></p>

                <script>
                function showAlert(msg) { alert(msg); }
                function updateInput(key) {
                    const payload = {
                        key,
                        name: document.getElementById('input-name-' + key).value,
                        min: document.getElementById('input-min-' + key).value,
                        max: document.getElementById('input-max-' + key).value,
                    };
                    fetch('/api/update_input', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    }).then(r => r.json()).then(j => showAlert(j.message));
                }
                function updateRelay(key) {
                    const payload = {
                        key,
                        name: document.getElementById('relay-name-' + key).value,
                        function: document.getElementById('relay-fn-' + key).value,
                        channel: document.getElementById('relay-channel-' + key).value,
                        setpoint: document.getElementById('relay-setpoint-' + key).value,
                    };
                    fetch('/api/update_relay', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(payload)
                    }).then(r => r.json()).then(j => showAlert(j.message));
                }
                </script>
                </body>
                </html>
            ''', inputs=inputs, relays=relays)

        @self.app.route('/history')
        def history():
            if 'username' not in session:
                return redirect(url_for('login'))
            export_dir = self.app_controller.get_export_status().get('path', 'exports')
            if not os.path.isdir(export_dir):
                files = []
            else:
                files = [f for f in os.listdir(export_dir) if f.endswith('.csv')]
            return render_template_string('''
                <!DOCTYPE html>
                <html>
                <head><title>Historial CSV</title></head>
                <body>
                <h1>Historial CSV</h1>
                <ul>
                {% for f in files %}
                    <li><a href="/history/{{ f }}">{{ f }}</a></li>
                {% endfor %}
                </ul>
                <p><a href="/dashboard">Sensores</a> | <a href="/relay">Relés</a> | <a href="/config">Configuración</a></p>
                </body>
                </html>
            ''', files=files)

        @self.app.route('/history/<path:filename>')
        def history_download(filename):
            export_dir = self.app_controller.get_export_status().get('path', 'exports')
            safe_name = os.path.basename(filename)
            return send_from_directory(export_dir, safe_name, as_attachment=True)

        @self.app.route('/export_status')
        def export_status():
            return jsonify(self.app_controller.get_export_status())

        @self.app.route('/api/update_input', methods=['POST'])
        def api_update_input():
            data = request.get_json(force=True)
            ok = self.app_controller.get_config().update_input(data.get('key'), data.get('name'), data.get('min'), data.get('max'))
            return jsonify({'success': ok, 'message': 'Input actualizado' if ok else 'Error al actualizar input'})

        @self.app.route('/api/update_relay', methods=['POST'])
        def api_update_relay():
            data = request.get_json(force=True)
            ok = self.app_controller.get_config().update_relay(data.get('key'), data.get('name'), data.get('function'), data.get('channel'), data.get('setpoint'))
            return jsonify({'success': ok, 'message': 'Relé actualizado' if ok else 'Error al actualizar relé'})

        @self.socketio.on('connect')
        def handle_connect():
            """Maneja conexión de cliente."""
            logger.info("WebServer", "Cliente conectado al dashboard")
            self._emit_sensor_data()
            self._emit_relay_status()

        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Maneja desconexión de cliente."""
            logger.info("WebServer", "Cliente desconectado del dashboard")

        @self.socketio.on('toggle_relay')
        def handle_toggle_relay(data):
            idx = data.get('index')
            if isinstance(idx, int):
                self.app_controller.relay_controller.toggle_manual_relay(idx)
                self.app_controller.relay_controller.evaluate_and_write()
                self._emit_relay_status()

        @self.socketio.on('request_status')
        def handle_request_status():
            self._emit_sensor_data()
            self._emit_relay_status()

        @self.app.route('/logout')
        def logout():
            session.pop('username', None)
            return redirect(url_for('login'))


    def _emit_sensor_data(self):
        """Emite datos actuales de sensores a todos los clientes conectados."""
        try:
            sensor_data = self.app_controller.get_all_sensors()
            self.socketio.emit('sensor_update', sensor_data)
        except Exception as e:
            logger.error("WebServer", f"Error emitiendo datos de sensores: {e}", exception=e)

    def _broadcast_loop(self):
        """Bucle para broadcast de datos cada 2 segundos."""
        while self.running:
            self._emit_sensor_data()
            time.sleep(2)  # Cada 2 segundos, igual que la lectura

    def start(self):
        """Inicia el servidor web en un hilo separado."""
        if self.running:
            logger.warning("WebServer", "Servidor ya está ejecutándose")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        logger.info("WebServer", "Servidor web iniciado")

    def stop(self):
        """Detiene el servidor web."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("WebServer", "Servidor web detenido")

    def _run_server(self):
        """Ejecuta el servidor Flask-SocketIO."""
        try:
            self.socketio.run(self.app, host=self.host, port=self.port, debug=False)
        except Exception as e:
            logger.error("WebServer", f"Error ejecutando servidor web: {e}", exception=e)
            self.running = False
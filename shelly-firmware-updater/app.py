from flask import Flask, jsonify, request, render_template_string
import requests
from concurrent.futures import ThreadPoolExecutor
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

IP_BASE = "192.168.5."  # Passe das Netzwerk an

def find_shellys():
    devices = []

    def check_ip(ip):
        try:
            url = f"http://{ip}/rpc/Shelly.CheckForUpdate"
            resp = requests.get(url, timeout=1)
            if resp.status_code == 200:
                data = resp.json()
                version = data.get("stable", {}).get("version")
                name = data.get("name", "Unbekannt")
                if version:
                    devices.append({"ip": ip, "version": version, "name": name})
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_ip, [f"{IP_BASE}{i}" for i in range(1, 255)])

    # Sortiere nach IP numerisch
    def ip_key(dev):
        return tuple(int(part) for part in dev["ip"].split('.'))
    devices.sort(key=ip_key)

    return devices


@app.route("/api/devices")
def api_devices():
    devices = find_shellys()
    return jsonify(devices)


@app.route("/api/update", methods=["POST"])
def api_update():
    ip = request.json.get("ip")
    if not ip:
        return jsonify({"success": False, "message": "IP-Adresse fehlt"}), 400
    try:
        resp = requests.get(f"http://{ip}/rpc/Shelly.Update", timeout=5)
        if resp.status_code == 200:
            return jsonify({"success": True, "message": f"Update gestartet für {ip}"})
        else:
            return jsonify({"success": False, "message": f"Fehler beim Update für {ip}: {resp.text}"}), 500
    except requests.RequestException as e:
        return jsonify({"success": False, "message": f"Netzwerkfehler: {str(e)}"}), 500


@app.route("/api/update_all", methods=["POST"])
def api_update_all():
    devices = find_shellys()
    results = []
    for device in devices:
        ip = device["ip"]
        try:
            resp = requests.get(f"http://{ip}/rpc/Shelly.Update", timeout=5)
            if resp.status_code == 200:
                results.append({"ip": ip, "success": True})
            else:
                results.append({"ip": ip, "success": False})
        except requests.RequestException:
            results.append({"ip": ip, "success": False})
    return jsonify(results)


@app.route("/")
def index():
    html = """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Shelly Firmware Updater</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f9f9f9;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        #loader {
            font-size: 1.2em;
            margin-top: 50px;
        }
        #loader span {
            margin-left: 10px;
        }
        table {
            width: 100%;
            max-width: 700px;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px 12px;
            text-align: left;
        }
        th {
            background: #eee;
        }
        button {
            padding: 6px 12px;
            background: #007bff;
            border: none;
            color: white;
            cursor: pointer;
            border-radius: 4px;
        }
        button:disabled {
            background: #999;
            cursor: not-allowed;
        }
        #topbar {
            width: 100%;
            max-width: 700px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div id="topbar">
        <div id="device-count">Gefundene Geräte: 0</div>
        <button id="update-all" disabled>Alle aktualisieren</button>
    </div>
    <div id="loader" style="display: none;">
        🔄 Shellys werden im Netzwerk gesucht...
    </div>
    <table id="device-table" style="display:none;">
        <thead>
            <tr>
                <th>IP-Adresse</th>
                <th>Name</th>
                <th>Version</th>
                <th>Update</th>
            </tr>
        </thead>
        <tbody id="device-tbody"></tbody>
    </table>

<script>
async function fetchDevices() {
    const loader = document.getElementById('loader');
    const table = document.getElementById('device-table');
    const tbody = document.getElementById('device-tbody');
    const deviceCount = document.getElementById('device-count');
    const updateAllBtn = document.getElementById('update-all');

    loader.style.display = 'block';
    table.style.display = 'none';
    updateAllBtn.disabled = true;
    deviceCount.textContent = "Gefundene Geräte: 0";

    try {
        const response = await fetch("api/devices");
        if (!response.ok) throw new Error(`Netzwerkantwort nicht OK: ${response.status}`);
        const devices = await response.json();

        loader.style.display = 'none';

        if (devices.length === 0) {
            deviceCount.textContent = "Keine Shelly-Geräte im Netzwerk gefunden.";
            updateAllBtn.disabled = true;
            table.style.display = 'none';
            return;
        }

        deviceCount.textContent = `Gefundene Geräte: ${devices.length}`;
        updateAllBtn.disabled = false;
        table.style.display = 'table';

        tbody.innerHTML = '';
        for (const device of devices) {
            const tr = document.createElement('tr');

            tr.innerHTML = `
                <td>${device.ip}</td>
                <td>${device.name || 'Unbekannt'}</td>
                <td>${device.version}</td>
                <td><button onclick="updateDevice('${device.ip}', this)">Update</button></td>
            `;
            tbody.appendChild(tr);
        }
    } catch (error) {
        loader.style.display = 'none';
        alert("Fehler beim Laden der Geräte: " + error.message);
    }
}

async function updateDevice(ip, button) {
    button.disabled = true;
    try {
        const resp = await fetch("api/update", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ip})
        });
        const result = await resp.json();
        alert(result.message);
    } catch (e) {
        alert("Fehler beim Update: " + e.message);
    } finally {
        button.disabled = false;
    }
}

document.getElementById('update-all').addEventListener('click', async () => {
    const btn = document.getElementById('update-all');
    btn.disabled = true;
    try {
        const resp = await fetch("api/update_all", { method: "POST" });
        const results = await resp.json();
        let successCount = results.filter(r => r.success).length;
        alert(`Updates gestartet für ${successCount} Geräte.`);
    } catch (e) {
        alert("Fehler beim Update aller Geräte: " + e.message);
    } finally {
        btn.disabled = false;
    }
});

window.onload = fetchDevices;
</script>
</body>
</html>
    """
    return render_template_string(html)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
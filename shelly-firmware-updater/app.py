from flask import Flask, jsonify, request, render_template_string
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

IP_BASE = "192.168.5."  # ggf. an eigenes Netz anpassen

def find_shellys():
    devices = []
    def check_ip(ip):
        try:
            name = "Unbekannt"
            try:
                r_info = requests.get(f"http://{ip}/rpc/Shelly.GetDeviceInfo", timeout=1)
                if r_info.status_code == 200:
                    name = r_info.json().get("name", name)
            except requests.RequestException:
                pass
            r_upd = requests.get(f"http://{ip}/rpc/Shelly.CheckForUpdate", timeout=1)
            if r_upd.status_code == 200:
                data = r_upd.json()
                version = data.get("stable", {}).get("version")
                if version:
                    devices.append({"ip": ip, "name": name, "version": version})
        except requests.RequestException:
            pass

    ips = [f"{IP_BASE}{i}" for i in range(1, 255)]
    with ThreadPoolExecutor(max_workers=50) as ex:
        ex.map(check_ip, ips)

    devices.sort(key=lambda d: tuple(int(p) for p in d["ip"].split(".")))
    return devices

@app.route("/api/devices")
def api_devices():
    return jsonify(find_shellys())

@app.route("/api/update", methods=["POST"])
def api_update():
    ip = request.json.get("ip")
    if not ip:
        return jsonify({"success": False, "message": "IP-Adresse fehlt"}), 400
    try:
        r = requests.get(f"http://{ip}/rpc/Shelly.Update", timeout=5)
        if r.status_code == 200:
            return jsonify({"success": True, "message": f"Update gestartet für {ip}"})
        return jsonify({"success": False, "message": f"Fehler beim Update für {ip}: {r.text}"}), 500
    except requests.RequestException as e:
        return jsonify({"success": False, "message": f"Netzwerkfehler: {e}"}), 500

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
    body { font-family: Arial, sans-serif; background:#f9f9f9; padding:20px; display:flex; flex-direction:column; align-items:center; }
    #loader { display:none; font-size:1.1em; margin-top:40px; }
    .spinner { border:8px solid #e9e9e9; border-top:8px solid #007BFF; border-radius:50%; width:48px; height:48px; animation:spin 1s linear infinite; margin:0 auto 12px; }
    @keyframes spin { 0%{transform:rotate(0)} 100%{transform:rotate(360deg)} }
    table { width:100%; max-width:900px; border-collapse:collapse; margin-top:20px; display:none; }
    th,td { border:1px solid #ccc; padding:10px; text-align:left; }
    th { background:#f4f4f4; }
    button { padding:6px 12px; background:#007BFF; border:none; color:#fff; cursor:pointer; border-radius:4px; }
    #topbar { width:100%; max-width:900px; display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }
    #error { color:red; font-weight:bold; display:none; }
</style>
</head>
<body>
    <div id="topbar">
        <div id="device-count">Gefundene Geräte: 0</div>
        <button id="update-all" disabled>Alle aktualisieren</button>
    </div>

    <div id="loader">
        <div class="spinner" aria-hidden="true"></div>
        <div>🔄 Shellys werden im Netzwerk gesucht...</div>
    </div>

    <div id="error"></div>

    <table id="device-table" aria-live="polite">
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
    const errorBox = document.getElementById('error');

    loader.style.display = 'block';
    table.style.display = 'none';
    errorBox.style.display = 'none';
    updateAllBtn.disabled = true;
    deviceCount.textContent = "Gefundene Geräte: 0";
    tbody.innerHTML = '';

    try {
        const resp = await fetch("api/devices"); // RELATIV für Ingress
        if (!resp.ok) throw new Error("Netzwerkantwort nicht OK: " + resp.status);
        const devices = await resp.json();

        loader.style.display = 'none';

        if (!devices || devices.length === 0) {
            deviceCount.textContent = "Keine Shelly-Geräte im Netzwerk gefunden.";
            table.style.display = 'none';
            return;
        }

        deviceCount.textContent = `Gefundene Geräte: ${devices.length}`;
        updateAllBtn.disabled = false;
        table.style.display = 'table';

        for (const d of devices) {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${d.ip}</td>
                <td>${d.name || 'Unbekannt'}</td>
                <td>${d.version || 'Unbekannt'}</td>
                <td><button onclick="updateDevice('${d.ip}', this)">Update</button></td>
            `;
            tbody.appendChild(tr);
        }
    } catch (e) {
        loader.style.display = 'none';
        errorBox.textContent = "Fehler beim Laden der Geräte: " + e.message;
        errorBox.style.display = 'block';
    }
}

async function updateDevice(ip, button) {
    button.disabled = true;
    try {
        const resp = await fetch("api/update", {
            method: "POST",
            headers: {"Content-Type":"application/json"},
            body: JSON.stringify({ ip })
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
        const ok = results.filter(r => r.success).length;
        alert(`Updates gestartet für ${ok} Geräte.`);
    } catch (e) {
        alert("Fehler beim Update aller Geräte: " + e.message);
    } finally {
        btn.disabled = false;
    }
});

window.addEventListener('load', fetchDevices);
</script>
</body>
</html>
    """
    return render_template_string(html)

# Für lokalen Test (im Add-on startet gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
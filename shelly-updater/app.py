from flask import Flask, render_template_string, request, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

def find_shellys():
    devices = []
    ip_base = "192.168.5."  # Anpassen

    def check_ip(ip):
        try:
            name = "Unbekannt"
            try:
                info_resp = requests.get(f"http://{ip}/rpc/Shelly.GetDeviceInfo", timeout=1)
                if info_resp.status_code == 200:
                    name = info_resp.json().get("name", name)
            except requests.RequestException:
                pass

            update_resp = requests.get(f"http://{ip}/rpc/Shelly.CheckForUpdate", timeout=1)
            if update_resp.status_code == 200:
                data = update_resp.json()
                version = data.get("stable", {}).get("version")
                if version:
                    devices.append({"ip": ip, "name": name, "version": version})
        except requests.RequestException:
            pass

    ips = [f"{ip_base}{i}" for i in range(1, 255)]
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_ip, ips)

    return devices

@app.route("/update", methods=["POST"])
def update_firmware():
    ip = request.json.get("ip")
    if not ip:
        return jsonify({"success": False, "message": "IP-Adresse fehlt"}), 400

    try:
        response = requests.get(f"http://{ip}/rpc/Shelly.Update", timeout=5)
        if response.status_code == 200:
            return jsonify({"success": True, "message": f"Update gestartet für {ip}"})
        else:
            return jsonify({"success": False, "message": f"Fehler beim Update für {ip}: {response.text}"}), 500
    except requests.RequestException as e:
        return jsonify({"success": False, "message": f"Netzwerkfehler: {str(e)}"}), 500

@app.route("/")
def index():
    html = """ 
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Shelly Gen.2 Firmware Updater</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f9f9f9;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                min-height: 100vh;
                box-sizing: border-box;
            }
            #loading {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 60vh;
                font-size: 18px;
                font-weight: bold;
                color: #333;
            }
            .loader {
                border: 8px solid #e9e9e9;
                border-top: 8px solid #007BFF;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                animation: spin 1s linear infinite;
                margin-bottom: 16px;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            table {
                width: 100%;
                max-width: 900px;
                border-collapse: collapse;
                margin-top: 20px;
                display: none;
            }
            th, td {
                border: 1px solid #ccc;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #f4f4f4;
            }
            button {
                padding: 5px 10px;
                background-color: #007BFF;
                color: white;
                border: none;
                cursor: pointer;
            }
            #error {
                color: red;
                font-weight: bold;
                display: none;
            }
        </style>
        <script>
            async function loadDevices() {
                const loading = document.getElementById("loading");
                const table = document.getElementById("device-table");
                const tbody = document.getElementById("table-body");
                const error = document.getElementById("error");

                loading.style.display = "flex";
                table.style.display = "none";
                error.style.display = "none";
                tbody.innerHTML = "";

                try {
                    const response = await fetch("/devices");
                    if (!response.ok) throw new Error("Netzwerkantwort nicht OK: " + response.status);
                    const devices = await response.json();

                    loading.style.display = "none";

                    if (!devices || devices.length === 0) {
                        error.innerText = "⚠️ Keine Shelly-Geräte im Netzwerk gefunden.";
                        error.style.display = "block";
                        return;
                    }

                    devices.forEach(device => {
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${device.ip}</td>
                            <td>${device.name || "Unbekannt"}</td>
                            <td>${device.version || "Unbekannt"}</td>
                            <td><button onclick="updateFirmware('${device.ip}')">Update</button></td>
                        `;
                        tbody.appendChild(row);
                    });

                    table.style.display = "table";
                } catch (err) {
                    loading.style.display = "none";
                    error.innerText = "Fehler beim Laden der Geräte: " + err.message;
                    error.style.display = "block";
                    console.error(err);
                }
            }

            async function updateFirmware(ip) {
                try {
                    const response = await fetch("/update", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({ ip })
                    });
                    const result = await response.json();
                    alert(result.message);
                } catch (error) {
                    alert("Fehler beim Update: " + error.message);
                }
            }

            window.addEventListener('load', loadDevices);
        </script>
    </head>
    <body>
        <div id="loading">
            <div class="loader" aria-hidden="true"></div>
            <div>🔍 Shellys werden im Netzwerk gesucht...</div>
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
            <tbody id="table-body"></tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/devices")
def devices_api():
    devices = find_shellys()
    def ip_key(device):
        return tuple(int(part) for part in device["ip"].split("."))
    devices.sort(key=ip_key)
    return jsonify(devices)

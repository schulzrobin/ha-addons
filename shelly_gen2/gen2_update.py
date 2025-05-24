from flask import Flask, render_template_string, request, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor

# Flask-App erstellen
app = Flask(__name__)

# Shelly-Geräte finden
def find_shellys():
    devices = []
    ip_base = "192.168.5."  # Passe dies an dein Netzwerk an
    def check_ip(ip):
        try:
            response = requests.get(f"http://{ip}/rpc/Shelly.CheckForUpdate", timeout=1)
            if response.status_code == 200:
                devices.append({"ip": ip, "info": response.json()})
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_ip, [f"{ip_base}{i}" for i in range(1, 255)])
    return devices

# Shelly-Firmware-Update auslösen
@app.route("/update", methods=["POST"])
def update_firmware():
    ip = request.json.get("ip")
    if not ip:
        return jsonify({"success": False, "message": "IP-Adresse fehlt"}), 400

    try:
        response = requests.get(f"http://{ip}/rpc/Shelly.Update", timeout=5)  # Shelly OTA-Update
        if response.status_code == 200:
            return jsonify({"success": True, "message": f"Update gestartet für {ip}"})
        else:
            return jsonify({"success": False, "message": f"Fehler beim Update für {ip}: {response.text}"}), 500
    except requests.RequestException as e:
        return jsonify({"success": False, "message": f"Netzwerkfehler: {str(e)}"}), 500

# Hauptseite
@app.route("/")
def index():
    devices = find_shellys()
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Shelly Finder</title>
        <style>
            table { width: 100%; border-collapse: collapse; }
            th, td { border: 1px solid #ccc; padding: 10px; text-align: left; }
            th { background-color: #f4f4f4; }
            button { padding: 5px 10px; background-color: #007BFF; color: white; border: none; cursor: pointer; }
            button:hover { background-color: #0056b3; }
        </style>
        <script>
            async function updateFirmware(ip) {
                try {
                    const response = await fetch("/update", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ ip })
                    });
                    const result = await response.json();
                    alert(result.message);
                } catch (error) {
                    alert("Fehler beim Update: " + error.message);
                }
            }
        </script>
    </head>
    <body>
        <h1>Shelly Geräte im Netzwerk</h1>
        <table>
            <tr>
                <th>IP-Adresse</th>
                <th>Geräteinformationen</th>
                <th>Firmware-Update</th>
            </tr>
            {% for device in devices %}
            <tr>
                <td>{{ device.ip }}</td>
                <td><pre>{{ device.info | tojson }}</pre></td>
                <td>
                    <button onclick="updateFirmware('{{ device.ip }}')">Update</button>
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    return render_template_string(html, devices=devices)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

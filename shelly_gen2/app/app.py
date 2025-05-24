from flask import Flask, render_template, request, jsonify
import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

app = Flask(__name__)

lock = Lock()

def find_shellys():
    devices = []
    ip_base = "192.168.5."  # Dein Netzwerk

    def check_ip(ip):
        try:
            update_response = requests.get(f"http://{ip}/rpc/Shelly.CheckForUpdate", timeout=3)
            config_response = requests.get(f"http://{ip}/rpc/Sys.GetConfig", timeout=3)
            if update_response.status_code == 200 and config_response.status_code == 200:
                update_data = update_response.json()
                config_data = config_response.json()

                version = update_data.get("stable", {}).get("version")
                name = config_data.get("device", {}).get("name", "Unbenannt")

                if version:
                    with lock:
                        devices.append({
                            "ip": ip,
                            "name": name,
                            "version": version
                        })
        except requests.RequestException:
            pass

    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(check_ip, [f"{ip_base}{i}" for i in range(1, 255)])
    return devices

@app.route("/api/devices")
def api_devices():
    return jsonify(find_shellys())

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
            return jsonify({"success": False, "message": f"Fehler beim Update: {response.text}"}), 500
    except requests.RequestException as e:
        return jsonify({"success": False, "message": f"Netzwerkfehler: {str(e)}"}), 500

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

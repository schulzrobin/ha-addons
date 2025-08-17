# Shelly Firmware Updater – Home Assistant Add-on

![Shelly Logo](https://user-images.githubusercontent.com/0000000/shelly-logo.png) <!-- optional: eigenes Logo einfügen -->

## Übersicht
Der **Shelly Firmware Updater** ist ein Home-Assistant-Add-on, das automatisch Shelly-Geräte im lokalen Netzwerk erkennt und deren Firmware aktualisieren kann – direkt aus der Home-Assistant-Oberfläche heraus.  
Es läuft vollständig über **Ingress**, sodass keine Portfreigaben oder separaten Weboberflächen nötig sind.

## Funktionen
- 🔍 **Netzwerkscan** – Durchsucht den angegebenen IP-Bereich (`ip_base`) nach Shelly-Geräten.
- 📦 **Firmware-Check** – Zeigt die aktuelle Firmwareversion an und erkennt Updates.
- ⬆️ **Update starten** – Einzel- oder Massenupdate der gefundenen Geräte.
- 🪵 **Persistente Logs** – Protokolliert alle Aktionen in `/data/logs/app.log`.
- 📱 **Responsive UI** – Funktioniert auf Desktop und Mobilgeräten.
- 🔒 **Ingress** – Läuft sicher im Home-Assistant-Supervisor.

## Screenshots
*(Füge hier Screenshots deiner UI ein, um den Ablauf zu zeigen)*

## Installation
### 1. Add-on-Verzeichnis erstellen
Kopiere die Add-on-Dateien in den Ordner `/addons/shelly-firmware-updater` auf deinem Home Assistant Host (z. B. per Samba oder SSH).

### 2. Add-on im Home Assistant hinzufügen
- **Einstellungen → Add-ons → Add-on-Store**
- Rechts oben auf **⋮ → Neu laden** klicken  
  (falls nicht sichtbar, im Benutzerprofil „Erweiterter Modus“ aktivieren)
- Das Add-on **Shelly Firmware Updater** sollte nun erscheinen.

### 3. Konfiguration
Beispielkonfiguration in der Add-on-UI:
```yaml
ip_base: "192.168.5."
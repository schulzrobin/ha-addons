### Shelly Firmware Updater

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
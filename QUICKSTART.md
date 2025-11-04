# Futterkarre-2 Quick Start Guide

## 🚀 Schnellstart

### Entwicklung (Simulation Mode)

```bash
# 1. Repository klonen
git clone https://github.com/DonKeWu/Futterkarre-1.2.git
cd Futterkarre-1.2

# 2. Abhängigkeiten installieren (optional für Entwicklung)
pip3 install PyQt5

# 3. Im Simulation Mode starten
FUTTERKARRE_SIMULATION=1 python3 main.py
```

### Tests ausführen

```bash
# Unit Tests
python3 -m unittest discover tests -v

# CLI Demo (ohne GUI)
python3 demo_cli.py
```

### Raspberry Pi Produktion

```bash
# 1. System vorbereiten
sudo apt-get update
sudo apt-get install python3-pyqt5 python3-pip

# 2. Repository klonen
git clone https://github.com/DonKeWu/Futterkarre-1.2.git
cd Futterkarre-1.2

# 3. Abhängigkeiten installieren
pip3 install -r requirements.txt

# 4. Konfiguration anpassen
nano config/settings.py
# Setzen Sie SIMULATION_MODE = False für echte Hardware

# 5. Anwendung starten
python3 main.py
```

## 📋 Was ist enthalten?

- **Touch GUI** für 1024x600 Display ✓
- **30 Pferde** verwalten ✓
- **HX711 Waage** Integration ✓
- **CSV Daten** Speicherung ✓
- **3 Futterarten**: Heu, Heulage, Pellets ✓

## 🎯 Hauptfunktionen

### 1. Wiegen (⚖️)
- Waage tarieren
- Live-Gewichtsanzeige
- Pferd und Futterart auswählen
- Fütterung aufzeichnen

### 2. Pferde (🐴)
- Pferde hinzufügen
- Daten bearbeiten
- Pferde löschen
- Übersicht aller Pferde

### 3. Historie (📊)
- Fütterungsverlauf
- Nach Pferd filtern
- Nach Zeitraum filtern
- Statistiken

## 🔧 Konfiguration

### Simulation Mode

**Option 1: Environment Variable (empfohlen)**
```bash
FUTTERKARRE_SIMULATION=1 python3 main.py
```

**Option 2: Config-Datei**
```python
# config/settings.py
SIMULATION_MODE = True
```

### Hardware Pins (HX711)

```python
# config/settings.py
HX711_DATA_PIN = 5   # BCM Pin 5
HX711_CLOCK_PIN = 6  # BCM Pin 6
```

### Display

```python
# config/settings.py
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
FULLSCREEN = True
```

## 📚 Dokumentation

| Datei | Inhalt |
|-------|--------|
| README.md | Vollständige Bedienungsanleitung |
| INSTALLATION.md | Detaillierte Installation |
| TESTING.md | Test-Prozeduren |
| ARCHITECTURE.md | Technische Architektur |

## 🐛 Fehlerbehebung

### Waage wird nicht erkannt
```bash
# Prüfen Sie GPIO-Berechtigungen
sudo usermod -a -G gpio $USER
# Neu einloggen erforderlich
```

### PyQt5 fehlt
```bash
# Auf Raspberry Pi
sudo apt-get install python3-pyqt5

# Auf anderen Systemen
pip3 install PyQt5
```

### Tests schlagen fehl
```bash
# Stellen Sie sicher, dass Sie im Projekt-Verzeichnis sind
cd /path/to/Futterkarre-1.2
python3 -m unittest discover tests -v
```

## 💡 Tipps

1. **Entwicklung**: Nutzen Sie Simulation Mode für schnelles Testen
2. **Backups**: Sichern Sie regelmäßig das `data/` Verzeichnis
3. **Kalibrierung**: Kalibrieren Sie die Waage regelmäßig
4. **Updates**: Prüfen Sie GitHub für neue Versionen

## 📞 Support

- **Issues**: https://github.com/DonKeWu/Futterkarre-1.2/issues
- **Dokumentation**: Siehe README.md und andere .md Dateien
- **Tests**: `python3 demo_cli.py` für schnelle Funktionsprüfung

## ✅ Checkliste für ersten Start

- [ ] Repository geklont
- [ ] Python 3.9+ installiert
- [ ] PyQt5 installiert (für GUI)
- [ ] Config angepasst (Simulation/Hardware)
- [ ] Tests durchgeführt (`python3 -m unittest discover tests`)
- [ ] CLI Demo getestet (`python3 demo_cli.py`)
- [ ] GUI gestartet (`python3 main.py`)
- [ ] Dokumentation gelesen (README.md)

## 🎉 Los geht's!

```bash
# Einfachster Start im Simulation Mode
FUTTERKARRE_SIMULATION=1 python3 main.py
```

Viel Erfolg mit Futterkarre-2! 🚜🐴

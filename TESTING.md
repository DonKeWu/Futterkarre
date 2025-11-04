# Testing Guide für Futterkarre-2

## Übersicht

Dieses Dokument beschreibt, wie die Futterkarre-2 Anwendung getestet werden kann.

## Unit Tests

### Tests ausführen

Alle Unit Tests ausführen:
```bash
python3 -m unittest discover tests -v
```

Einzelne Test-Module:
```bash
# Model-Tests
python3 -m unittest tests.test_models -v

# Hardware-Tests
python3 -m unittest tests.test_hardware -v
```

### Test-Abdeckung

Die Tests decken folgende Komponenten ab:

#### Models (src/models/)
- ✓ Horse: Erstellung, Serialisierung, Deserialisierung
- ✓ FeedRecord: Erstellung, Serialisierung, Deserialisierung
- ✓ DataManager: CRUD-Operationen für Pferde und Fütterungshistorie

#### Hardware (src/hardware/)
- ✓ SimulatedScale: Initialisierung, Tarieren, Wiegungen, Kalibrierung

## CLI Demo

Eine interaktive Demonstration ohne GUI:

```bash
python3 demo_cli.py
```

Die Demo zeigt:
1. Datenmodell-Operationen
2. Waagen-Simulation
3. CSV-Datenpersistenz
4. Kompletten Fütterungsworkflow

## GUI Tests (manuelle Tests)

### Voraussetzungen

Auf einem System mit PyQt5 (idealerweise Raspberry Pi):

```bash
pip3 install PyQt5
```

### Simulation Mode

Für Tests ohne Hardware-Waage:

1. Öffnen Sie `config/settings.py`
2. Setzen Sie: `SIMULATION_MODE = True`
3. Starten Sie die Anwendung: `python3 main.py`

### Test-Szenarien

#### 1. Pferdeverwaltung testen

1. Navigieren Sie zu "🐴 Pferde"
2. Klicken Sie "+ Neues Pferd"
3. Füllen Sie die Felder aus:
   - Name: "Testpferd"
   - Rasse: "Hannoveraner"
   - Alter: 5
   - Gewicht: 500
4. Klicken Sie "Speichern"
5. Verifizieren Sie, dass das Pferd in der Liste erscheint
6. Klicken Sie "✏️" zum Bearbeiten
7. Ändern Sie das Alter auf 6
8. Speichern und verifizieren Sie die Änderung
9. Optional: Klicken Sie "🗑️" zum Löschen (mit Vorsicht!)

**Erwartetes Ergebnis:**
- Pferd wird korrekt hinzugefügt
- Änderungen werden gespeichert
- Tabelle wird aktualisiert

#### 2. Wiegefunktion testen

1. Navigieren Sie zu "⚖️ Wiegen"
2. Klicken Sie "Tarieren"
3. Verifizieren Sie, dass das Gewicht ~0.00 kg anzeigt
4. In Simulation Mode: Das Gewicht variiert leicht (Noise-Simulation)
5. Wählen Sie ein Pferd aus der Liste
6. Wählen Sie eine Futterart (z.B. "Heu")
7. Im Simulation Mode können Sie das Gewicht nicht manuell ändern
   - In echter Hardware: Legen Sie Futter auf die Waage
8. Geben Sie optional Notizen ein
9. Klicken Sie "✓ Speichern"

**Erwartetes Ergebnis:**
- Tarieren setzt das Gewicht auf ~0
- Gewicht wird kontinuierlich aktualisiert (alle 500ms)
- Speichern zeigt Erfolgsmeldung
- Daten werden in CSV gespeichert

#### 3. Historie testen

1. Navigieren Sie zu "📊 Historie"
2. Verifizieren Sie, dass alle Fütterungen angezeigt werden
3. Testen Sie die Filter:
   - Wählen Sie ein spezifisches Pferd
   - Wählen Sie verschiedene Zeiträume (Heute, 7 Tage, etc.)
4. Überprüfen Sie die Statistiken:
   - Gesamtanzahl Fütterungen
   - Gesamtmenge in kg

**Erwartetes Ergebnis:**
- Alle Einträge werden korrekt angezeigt
- Filter funktionieren
- Statistiken sind korrekt

#### 4. Touch-Bedienung testen (auf Raspberry Pi)

1. Testen Sie alle Buttons mit Finger-Touch
2. Verifizieren Sie, dass Dropdowns funktionieren
3. Testen Sie Textfeld-Eingabe mit virtueller Tastatur
4. Überprüfen Sie die Lesbarkeit auf 7" Display

**Erwartetes Ergebnis:**
- Alle Buttons reagieren auf Touch
- Text ist gut lesbar
- Interface ist intuitiv bedienbar

### Automatisierte GUI-Tests (optional)

Für fortgeschrittene Benutzer mit pytest-qt:

```bash
pip3 install pytest-qt
```

Hinweis: GUI-Tests sind aktuell nicht implementiert, können aber bei Bedarf hinzugefügt werden.

## Hardware-Tests (mit echter Waage)

### Voraussetzungen

- Raspberry Pi mit HX711 und Wägezelle
- Korrekte Verkabelung (siehe INSTALLATION.md)
- `SIMULATION_MODE = False` in `config/settings.py`

### Test-Prozedur

#### 1. Hardware-Verbindung testen

```bash
# Einfaches Test-Skript erstellen
cat > test_hardware.py << 'EOF'
from src.hardware import HX711Scale

scale = HX711Scale()
if scale.initialize():
    print("✓ Hardware erfolgreich initialisiert")
    print(f"✓ Scale ready: {scale.is_ready()}")
    
    # Test Tare
    if scale.tare():
        print("✓ Tarieren erfolgreich")
    
    # Test Reading
    weight = scale.get_weight()
    if weight is not None:
        print(f"✓ Gewicht: {weight:.2f} kg")
    else:
        print("✗ Fehler beim Wiegen")
    
    scale.cleanup()
else:
    print("✗ Hardware-Initialisierung fehlgeschlagen")
EOF

python3 test_hardware.py
```

#### 2. Kalibrierung testen

1. Entfernen Sie alle Lasten von der Waage
2. Starten Sie die Anwendung
3. Tarieren Sie die Waage
4. Legen Sie ein bekanntes Gewicht auf (z.B. 5.0 kg)
5. Überprüfen Sie die Anzeige
6. Bei Abweichung: Kalibrieren Sie neu (siehe INSTALLATION.md)

**Akzeptabler Fehler:**
- ±0.05 kg bei Gewichten bis 10 kg
- ±0.1 kg bei Gewichten über 10 kg

#### 3. Stabilität testen

Lassen Sie ein konstantes Gewicht auf der Waage:
- Beobachten Sie die Anzeige für 1 Minute
- Variationen sollten < ±0.02 kg sein

#### 4. Wiederholbarkeit testen

1. Tarieren Sie die Waage
2. Legen Sie 5kg auf
3. Notieren Sie den Wert
4. Entfernen Sie das Gewicht
5. Wiederholen Sie 10x
6. Berechnen Sie Standardabweichung

**Akzeptabel:** Standardabweichung < 0.03 kg

## Daten-Persistenz testen

### CSV-Dateien überprüfen

```bash
# Pferde-Datenbank
cat data/horses.csv

# Fütterungshistorie
cat data/feed_records.csv
```

### Backup und Restore testen

```bash
# Backup erstellen
cp -r data/ data_backup/

# Daten löschen
rm data/*.csv

# Anwendung starten (erstellt leere Dateien)
python3 main.py
# (Beenden Sie die Anwendung)

# Restore
cp data_backup/*.csv data/

# Verifizieren Sie, dass Daten wieder da sind
python3 main.py
```

## Performance-Tests

### GUI-Reaktionszeit

- Button-Klicks sollten < 100ms reagieren
- View-Wechsel sollte < 200ms dauern
- Tabellen-Refresh sollte < 500ms dauern

### Daten-Operationen

```bash
# Performance-Test-Skript
cat > test_performance.py << 'EOF'
import time
from src.models import DataManager, Horse, FeedRecord
from datetime import datetime

dm = DataManager()

# Test: 100 Pferde hinzufügen
start = time.time()
for i in range(100):
    horse = Horse(i, f"Horse_{i}", "Testbreed")
    dm.add_horse(horse)
duration = time.time() - start
print(f"100 Pferde hinzufügen: {duration:.2f}s")

# Test: Alle Pferde laden
start = time.time()
horses = dm.get_all_horses()
duration = time.time() - start
print(f"100 Pferde laden: {duration:.3f}s")
print(f"Geladen: {len(horses)} Pferde")

# Aufräumen
import os
os.remove("data/horses.csv")
os.remove("data/feed_records.csv")
EOF

python3 test_performance.py
```

**Erwartete Performance:**
- 100 Pferde hinzufügen: < 0.5s
- 100 Pferde laden: < 0.1s

## Fehlerbehandlung testen

### Ungültige Eingaben

1. Versuchen Sie, ein Pferd ohne Namen hinzuzufügen
2. Versuchen Sie, negative Gewichte zu speichern
3. Versuchen Sie, ungültige Futterarten auszuwählen

**Erwartetes Ergebnis:** Angemessene Fehlermeldungen

### Hardware-Fehler simulieren

```python
# In einer Python-Konsole
from src.controllers import AppController

controller = AppController()
# Simulieren Sie einen Hardware-Fehler
controller.scale = None
weight = controller.get_current_weight()
print(weight)  # Sollte None sein
```

## Langzeit-Tests

### 24-Stunden-Test (optional)

1. Starten Sie die Anwendung im Dauerbetrieb
2. Führen Sie alle 2 Stunden eine Fütterung durch
3. Überprüfen Sie:
   - Speicher-Verbrauch (sollte stabil bleiben)
   - CPU-Last (sollte < 5% im Idle sein)
   - Keine Abstürze
   - Alle Daten korrekt gespeichert

```bash
# Speicher-Überwachung
top -p $(pgrep -f main.py)
```

## Test-Checkliste

Vor einem Release sollten alle folgenden Tests erfolgreich sein:

- [ ] Alle Unit Tests bestehen
- [ ] CLI Demo läuft ohne Fehler
- [ ] GUI startet im Simulation Mode
- [ ] Pferdeverwaltung: Hinzufügen, Bearbeiten, Löschen
- [ ] Wiegefunktion: Tarieren, Messen, Speichern
- [ ] Historie: Anzeige, Filterung, Statistiken
- [ ] CSV-Dateien werden korrekt erstellt und gelesen
- [ ] Hardware-Tests (falls Hardware vorhanden)
- [ ] Touch-Bedienung funktioniert
- [ ] Performance ist akzeptabel
- [ ] Fehlerbehandlung funktioniert
- [ ] Keine Memory Leaks im Dauerbetrieb

## Probleme melden

Bei Problemen während der Tests:
1. Notieren Sie die genauen Schritte zur Reproduktion
2. Sammeln Sie relevante Logs und Fehlermeldungen
3. Erstellen Sie ein Issue auf GitHub
4. Fügen Sie Ihre Systemkonfiguration hinzu

## Test-Umgebungen

### Entwicklung
- Python 3.9+
- Beliebiges OS mit PyQt5
- Simulation Mode

### Staging
- Raspberry Pi 4/5
- Raspberry Pi OS
- Simulation Mode oder echte Hardware

### Produktion
- Raspberry Pi 5
- Raspberry Pi OS
- Echte HX711 Hardware
- 7" Touchscreen

---

**Viel Erfolg beim Testen! 🧪**

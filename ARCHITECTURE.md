# Futterkarre-2 Architektur-Dokumentation

## Überblick

Futterkarre-2 ist eine industrietaugliche PyQt5-Anwendung zur Futterverwaltung für Pferde, optimiert für Raspberry Pi 5 mit 7" Touchscreen.

## Architektur-Prinzipien

### MVC Pattern (Model-View-Controller)

Die Anwendung folgt strikt dem MVC-Pattern für klare Trennung der Verantwortlichkeiten:

```
┌─────────────────────────────────────────────────────────┐
│                         View                             │
│  (PyQt5 GUI - Benutzerinteraktion)                      │
│  • MainWindow                                            │
│  • WeighingView                                          │
│  • HorseManagementView                                   │
│  • HistoryView                                           │
└─────────────────┬───────────────────────────────────────┘
                  │
                  │ Qt Signals/Slots
                  │ Method Calls
                  ▼
┌─────────────────────────────────────────────────────────┐
│                      Controller                          │
│  (Anwendungslogik & Koordination)                       │
│  • AppController                                         │
│    - Koordiniert Model & Hardware                        │
│    - Geschäftslogik                                      │
│    - Event Handling                                      │
└─────────┬───────────────────────────┬───────────────────┘
          │                           │
          │                           │
          ▼                           ▼
┌───────────────────────┐   ┌────────────────────────────┐
│       Model           │   │      Hardware Layer        │
│  (Datenstrukturen)    │   │  (Hardware Abstraktion)    │
│  • Horse              │   │  • ScaleInterface (ABC)    │
│  • FeedRecord         │   │  • HX711Scale              │
│  • DataManager        │   │  • SimulatedScale          │
└───────┬───────────────┘   └────────────────────────────┘
        │
        │ CSV-Persistenz
        ▼
┌───────────────────────┐
│    Data Storage       │
│  • horses.csv         │
│  • feed_records.csv   │
└───────────────────────┘
```

## Komponenten-Übersicht

### 1. Configuration Layer (`config/`)

**Zweck:** Zentrale Konfiguration der Anwendung

**Dateien:**
- `settings.py`: Alle Anwendungseinstellungen
  - Display-Konfiguration (1024x600)
  - HX711 GPIO-Pins
  - Datenbank-Pfade
  - UI-Farben und Schriften
  - Mess-Parameter

**Design-Entscheidungen:**
- Alle Einstellungen an einem Ort
- Einfacher Wechsel zwischen Simulation/Hardware
- Umgebungsspezifische Anpassungen möglich

### 2. Model Layer (`src/models/`)

**Zweck:** Datenstrukturen und Persistenz

#### 2.1 Horse (`horse.py`)
```python
@dataclass
class Horse:
    horse_id: int
    name: str
    breed: Optional[str]
    age: Optional[int]
    weight: Optional[float]
    notes: Optional[str]
```

**Verantwortlichkeiten:**
- Repräsentiert ein Pferd
- Serialisierung zu/von CSV
- Validierung (implizit durch Typen)

#### 2.2 FeedRecord (`feed_record.py`)
```python
@dataclass
class FeedRecord:
    record_id: Optional[int]
    horse_id: int
    feed_type: str
    weight: float
    timestamp: datetime
    notes: Optional[str]
```

**Verantwortlichkeiten:**
- Repräsentiert eine Fütterung
- Zeitstempel-Management
- CSV-Serialisierung

#### 2.3 DataManager (`data_manager.py`)

**Verantwortlichkeiten:**
- CRUD-Operationen für Horses
- CRUD-Operationen für FeedRecords
- CSV-Datei-Management
- Datenintegrität

**API-Übersicht:**
```python
# Horse Management
get_all_horses() -> List[Horse]
get_horse_by_id(id) -> Optional[Horse]
add_horse(horse) -> bool
update_horse(horse) -> bool
delete_horse(id) -> bool

# Feed Record Management
get_all_feed_records(horse_id=None) -> List[FeedRecord]
add_feed_record(record) -> bool
get_feed_records_by_date_range(start, end, horse_id=None)
```

**Design-Entscheidungen:**
- CSV für Einfachheit und Portabilität
- Datei-basierte Persistenz (kein DB-Server nötig)
- Atomare Operationen für Datenintegrität

### 3. Hardware Layer (`src/hardware/`)

**Zweck:** Hardware-Abstraktion für Wägezellen

#### 3.1 ScaleInterface (`scale_interface.py`)

Abstract Base Class für alle Scale-Implementierungen:

```python
class ScaleInterface(ABC):
    @abstractmethod
    def initialize() -> bool
    
    @abstractmethod
    def tare() -> bool
    
    @abstractmethod
    def get_weight() -> Optional[float]
    
    @abstractmethod
    def calibrate(known_weight) -> bool
    
    @abstractmethod
    def cleanup()
    
    @abstractmethod
    def is_ready() -> bool
```

**Design-Vorteile:**
- Austauschbare Implementierungen
- Einfaches Testen ohne Hardware
- Erweiterbar für andere Waagen-Typen

#### 3.2 HX711Scale (`hx711_scale.py`)

Echte Hardware-Implementierung:

**Features:**
- GPIO-Kommunikation mit HX711
- Kalibrierung mit bekannten Gewichten
- Noise-Reduktion durch Mehrfach-Messungen
- Fehlerbehandlung

**GPIO-Konfiguration:**
- BCM Pin 5 (Data)
- BCM Pin 6 (Clock)

#### 3.3 SimulatedScale (`simulated_scale.py`)

Simulation für Entwicklung:

**Features:**
- Realistisches Verhalten
- Simuliertes Sensor-Rauschen
- Kontrollierbare Gewichte für Tests
- Keine Hardware-Abhängigkeiten

### 4. Controller Layer (`src/controllers/`)

#### AppController (`app_controller.py`)

Zentrale Anwendungslogik:

**Verantwortlichkeiten:**
1. Model-Koordination
2. Hardware-Management
3. Geschäftslogik-Validierung
4. Event-Distribution (Qt Signals)

**Qt Signals:**
```python
weight_updated = pyqtSignal(float)
scale_ready = pyqtSignal(bool)
error_occurred = pyqtSignal(str)
```

**API-Kategorien:**
1. **Horse Management**: CRUD-Operationen
2. **Scale Operations**: Waagen-Steuerung
3. **Feed Recording**: Fütterung aufzeichnen
4. **Data Retrieval**: Historie und Statistiken

**Design-Pattern:**
- Facade Pattern für vereinfachte API
- Observer Pattern via Qt Signals
- Dependency Injection (Scale)

### 5. View Layer (`src/views/`)

**Zweck:** PyQt5 GUI-Komponenten

#### 5.1 MainWindow (`main_window.py`)

Haupt-Anwendungsfenster:

**Struktur:**
```
┌────────────────────────────────────────┐
│  Header (App-Name, Status)             │ 60px
├────────────────────────────────────────┤
│  Navigation (Wiegen, Pferde, Historie) │ 70px
├────────────────────────────────────────┤
│                                        │
│  Stacked Widget (Views)                │ Flex
│                                        │
├────────────────────────────────────────┤
│  Status Bar                            │ 25px
└────────────────────────────────────────┘
```

**Features:**
- Vollbild für Touchscreen (1024x600)
- View-Management mit QStackedWidget
- Globaler Status-Indikator
- Navigation mit großen Buttons

#### 5.2 WeighingView (`weighing_view.py`)

Wiege-Interface:

**Komponenten:**
1. **Gewichts-Anzeige**: Große LCD-Style Anzeige (48pt)
2. **Tarieren-Button**: Waage nullen
3. **Auswahl**: Pferd + Futterart (Dropdowns)
4. **Speichern-Button**: Fütterung aufzeichnen
5. **Notizen-Feld**: Optionale Anmerkungen

**Features:**
- Live-Update (500ms Timer)
- Touch-optimierte Buttons (min. 50px Höhe)
- Validierung vor dem Speichern

#### 5.3 HorseManagementView (`horse_management_view.py`)

Pferde-CRUD-Interface:

**Features:**
- Tabellen-Ansicht aller Pferde
- Inline-Aktions-Buttons (✏️ Bearbeiten, 🗑️ Löschen)
- Dialog für Hinzufügen/Bearbeiten
- Auto-Refresh nach Änderungen

**Dialog-Felder:**
- Name* (Pflichtfeld)
- Rasse
- Alter
- Gewicht (kg)
- Notizen

#### 5.4 HistoryView (`history_view.py`)

Historie und Statistiken:

**Features:**
1. **Filter-Sektion**:
   - Pferd-Auswahl
   - Zeitraum (Heute, 7 Tage, Monat, Alle)
   
2. **Statistiken**:
   - Gesamtanzahl Fütterungen
   - Gesamtgewicht
   
3. **Historie-Tabelle**:
   - Datum/Zeit
   - Pferdename
   - Futterart
   - Menge
   - Notizen

**Design:**
- Sortierung: Neueste zuerst
- Echtzeit-Filterung
- Kompakte Darstellung

## Datenfluss

### Beispiel: Fütterung aufzeichnen

```
1. User: Klickt "Speichern" (WeighingView)
   │
   ▼
2. WeighingView.on_record_clicked()
   - Validiert Eingaben
   - Sammelt Daten (horse_id, feed_type, weight, notes)
   │
   ▼
3. AppController.record_feeding(...)
   - Validiert Geschäftsregeln
   - Erstellt FeedRecord-Objekt
   │
   ▼
4. DataManager.add_feed_record(...)
   - Generiert record_id
   - Serialisiert zu CSV
   - Schreibt in feed_records.csv
   │
   ▼
5. Rückmeldung an User
   - Success-Message
   - View-Aktualisierung
```

## Threading-Modell

**Single-threaded mit Qt Event Loop:**
- Alle GUI-Operationen im Main Thread
- Weight Updates via QTimer (500ms)
- Blocking-Operationen vermieden

**Warum kein Multi-Threading?**
- CSV-Operationen sind schnell genug
- Weniger Komplexität
- Keine Race Conditions
- Ausreichend für Use Case

## Fehlerbehandlung

### Strategie

1. **Validierung auf View-Ebene**:
   - Pflichtfelder
   - Wertebereich
   - Format

2. **Geschäftslogik im Controller**:
   - Datenintegrität
   - Konsistenz-Prüfungen
   - Hardware-Status

3. **Persistenz im Model**:
   - File I/O Errors
   - CSV-Format-Fehler

### Error Reporting

```python
# Via Qt Signals
controller.error_occurred.emit("Fehler-Text")

# Via Message Boxes
QMessageBox.warning(self, "Titel", "Nachricht")
```

## Performance-Überlegungen

### Optimierungen

1. **CSV-Caching**: Daten nur bei Bedarf neu laden
2. **Batch-Operations**: Mehrfache Änderungen in einem Write
3. **Lazy Loading**: Views laden Daten nur bei Anzeige
4. **Timer-Intervalle**: Balance zwischen Aktualität und CPU-Last

### Benchmarks (Target)

- App-Start: < 2 Sekunden
- View-Switch: < 200ms
- 100 Pferde laden: < 100ms
- Weight Update: < 50ms
- CSV Write: < 50ms

## Skalierbarkeit

### Aktuelle Limits

- Max. 30 Pferde (konfigurierbar)
- Unbegrenzte Feed Records (CSV-Größe)
- Single-User (Kein Concurrent Access)

### Erweiterungsmöglichkeiten

1. **Mehr Pferde**: `MAX_HORSES` in settings.py erhöhen
2. **Datenbank**: DataManager gegen SQL-Backend austauschen
3. **Netzwerk**: REST API für Multi-Device Support
4. **Cloud**: Daten-Synchronisation
5. **Analytics**: Erweiterte Auswertungen

## Sicherheit

### Aktuelle Maßnahmen

1. **Input Validation**: Alle User-Eingaben validiert
2. **Type Safety**: Python Type Hints
3. **GPIO Access**: Nur autorisierte Prozesse
4. **File Permissions**: CSV-Dateien geschützt

### Empfohlene Zusatzmaßnahmen (Produktion)

1. Regelmäßige Backups
2. Checksummen für Daten-Integrität
3. Audit-Log für Änderungen
4. User-Authentication (bei Multi-User)

## Testing-Strategie

### Test-Pyramide

```
     ┌─────────────┐
     │   Manual    │  GUI, Touch, Hardware
     │   Tests     │
     ├─────────────┤
     │ Integration │  Controller + Model
     │   Tests     │
     ├─────────────┤
     │    Unit     │  Models, Hardware
     │   Tests     │  (umfangreich)
     └─────────────┘
```

### Coverage

- **Unit Tests**: Models, Hardware Abstraction
- **Integration Tests**: Controller-Logic
- **Manual Tests**: GUI, Hardware, Touch

## Deployment

### Entwicklung

```bash
SIMULATION_MODE = True
python3 main.py
```

### Staging (Raspberry Pi Test)

```bash
SIMULATION_MODE = True
python3 main.py
# Test auf echter Hardware ohne Waage
```

### Produktion (Raspberry Pi + Hardware)

```bash
SIMULATION_MODE = False
python3 main.py
# oder als systemd Service
```

## Wartung

### Regelmäßige Aufgaben

1. **Daten-Backup**: Täglich `data/` sichern
2. **Log-Review**: Error-Logs prüfen
3. **Kalibrierung**: Monatlich Waage kalibrieren
4. **Updates**: Software-Updates installieren

### Monitoring

- Disk Space: CSV-Dateien wachsen
- Memory: Sollte stabil bleiben
- CPU: < 5% im Idle

## Erweiterungen

### Geplante Features (Roadmap)

1. **Export-Funktion**: CSV/PDF Export
2. **Grafische Statistiken**: Charts und Diagramme
3. **Fütterungsplan**: Automatische Empfehlungen
4. **Mehrsprachigkeit**: i18n Support
5. **Cloud-Backup**: Automatische Datensicherung

### Architektur-Vorbereitung

Die Architektur ist bereits vorbereitet für:
- Weitere Scale-Typen (via ScaleInterface)
- Zusätzliche Views (via Stacked Widget)
- Alternative Persistenz (via DataManager Interface)

## Technologie-Stack

| Layer | Technologie | Version |
|-------|-------------|---------|
| GUI | PyQt5 | 5.15+ |
| Language | Python | 3.9+ |
| Hardware | RPi.GPIO | 0.7.1+ |
| Sensor | HX711 | 1.1.2+ |
| Data | CSV | stdlib |
| OS | Raspberry Pi OS | Debian 12+ |

## Lessons Learned

### Was gut funktioniert

1. MVC-Pattern: Klare Struktur
2. Hardware-Abstraktion: Einfaches Testen
3. CSV-Persistenz: Einfach und robust
4. Qt Signals: Entkoppelte Kommunikation

### Was verbessert werden könnte

1. Unit Test Coverage für Views
2. Automatische GUI-Tests
3. Performance-Monitoring
4. Error-Logging in Datei

---

**Dokumentation Version:** 1.0  
**Erstellt:** November 2024  
**Für Futterkarre-2 Version:** 2.0.0

# Hardware-Beschaffungsliste für Futterkarre 2.0 Pi5-System

## Kernkomponenten

### 🖥️ **Raspberry Pi 5 System**
- **Raspberry Pi 5 (8GB RAM)** - Hauptcomputer
  - Modell: Raspberry Pi 5 Model B
  - RAM: 8GB LPDDR4X-4267
  - CPU: 2.4GHz Quad-core 64-bit Arm Cortex-A76
  - GPU: VideoCore VII, OpenGL ES 3.1, Vulkan 1.2
  - Preis: ~€90-100

### 📱 **Display & Eingabe**
- **7" Touchscreen Display**
  - Offizieller Pi 7" Touchscreen (1024x600)
  - oder: Waveshare 7" HDMI LCD (1024x600) mit Touch
  - Kapazitiv Touch für bessere Präzision
  - Preis: ~€70-90

### ⚖️ **Wägesystem (4x HX711)**
- **4x HX711 Wägezellen-Verstärker**
  - 24-Bit ADC für hohe Präzision
  - Versorgung: 5V oder 3.3V
  - Interface: Digital (SPI-ähnlich)
  - Preis: ~€6-8 pro Stück = €24-32

- **4x Wägezellen (Load Cells)**
  - Typ: S-Type oder Single Point
  - Kapazität: 50kg oder 100kg (je nach Anforderung)
  - Schutzart: IP65 oder höher
  - Material: Aluminium oder Edelstahl
  - Preis: ~€15-25 pro Stück = €60-100

### 🔋 **Stromversorgung**
- **LiFePO4 Akku (20Ah)**
  - Spannung: 12V
  - Kapazität: 20Ah (ca. 240Wh)
  - Typ: LiFePO4 (langlebig, sicher)
  - Mit BMS (Battery Management System)
  - Preis: ~€100-150

- **DC-DC Wandler**
  - Input: 12V (Akku)
  - Output: 5V/3A für Raspberry Pi
  - Effizienz: >90%
  - Schutzfunktionen
  - Preis: ~€15-25

### 🏠 **Gehäuse & Schutz**
- **Industriegehäuse IP65**
  - Material: ABS oder Polycarbonat
  - Größe: ca. 200x300x100mm
  - Schutzart: IP65 (staub-/wasserdicht)
  - Kabeldurchführungen
  - Preis: ~€50-80

## Verkabelung & Zubehör

### 🔌 **Kabel & Stecker**
- **Sensorkabel**
  - 4x Kabel für Wägezellen (4-6 Adern)
  - Länge: 3-5m (je nach Montage)
  - Stecker: M12 oder Schraubklemmen
  - Preis: ~€40-60

- **Stromkabel**
  - 12V Hauptstromkabel
  - USB-C Kabel für Pi5
  - Sicherung und Schalter
  - Preis: ~€20-30

### 🔧 **Montage & Befestigung**
- **Montagematerial**
  - Halterungen für Wägezellen
  - Vibrationsdämpfer
  - Schrauben/Befestigung
  - DIN-Hutschienen-Adapter
  - Preis: ~€30-50

## Optionale Erweiterungen

### 📡 **Kommunikation**
- **WLAN/Bluetooth** (bereits in Pi5 integriert)
- **4G/LTE Modul** (optional für Remote-Zugriff)
  - SIM7600G-H 4G HAT
  - Preis: ~€60-80

### 🔊 **Audio & Signale**
- **Lautsprecher** (für Feedback-Töne)
- **Status-LEDs** (Betrieb, Fehler, etc.)
- **Summer/Buzzer** (Alarme)
- Preis: ~€20-30

## Kostenübersicht

| Komponente | Kosten (€) |
|------------|------------|
| Raspberry Pi 5 (8GB) | 90-100 |
| 7" Touchscreen | 70-90 |
| 4x HX711 Module | 24-32 |
| 4x Wägezellen | 60-100 |
| LiFePO4 Akku (20Ah) | 100-150 |
| DC-DC Wandler | 15-25 |
| Industriegehäuse IP65 | 50-80 |
| Kabel & Verkabelung | 60-90 |
| Montage & Befestigung | 30-50 |
| **Gesamt Kernkomponenten** | **499-717** |
| Optionale Erweiterungen | 80-110 |
| **Total mit Optionen** | **579-827** |

## Empfohlene Lieferanten

### 🛒 **Deutschland**
- **Reichelt Elektronik** - Grundkomponenten, Pi5
- **Conrad Electronic** - Gehäuse, Akku, Kabel
- **Mouser Electronics** - HX711, Wägezellen
- **Amazon/eBay** - Komplett-Sets, günstige Optionen

### 🌍 **International**
- **RS Components** - Industriekomponenten
- **Farnell** - Raspberry Pi, offizielle Komponenten
- **AliExpress** - Günstige HX711/Wägezellen Sets

## Montage-Planung

### 📐 **Mechanischer Aufbau**
1. **Wägezellen-Position**: 4 Ecken der Karre
2. **Plattform**: Stabile Auflagefläche
3. **Gehäuse-Montage**: Geschützt aber zugänglich
4. **Kabelführung**: Ordentlich und geschützt

### ⚡ **Elektrische Installation**
1. **Stromversorgung**: 12V → 5V Wandlung
2. **Sensorverkabelung**: Shielded Cables
3. **Erdung**: Gemeinsame Masse
4. **Entstörung**: Ferrit-Kerne bei Bedarf

## Software-Vorbereitung

### 🐧 **Raspberry Pi OS Setup**
- Raspberry Pi OS (64-bit)
- Python 3.11+
- PyQt5/6 für GUI
- SQLite für Datenbank
- Git für Updates

### 📦 **Abhängigkeiten**
```bash
# System packages
sudo apt update
sudo apt install python3-pyqt5 python3-pip sqlite3

# Python packages
pip install RPi.GPIO hx711 pyqt5
```

## Implementierungs-Roadmap

### Phase 1: Grundsystem (Woche 1-2)
- ✅ Pi5 + Display Setup
- ✅ Grundsoftware Installation
- ✅ HX711 Hardware-Test

### Phase 2: Integration (Woche 3-4)
- ✅ Wägezellen Kalibrierung
- ✅ GUI Tests auf Hardware
- ✅ Stromversorgung optimieren

### Phase 3: Produktive Installation (Woche 5-6)
- ✅ Gehäuse-Montage
- ✅ Feldtests
- ✅ Feinabstimmung

## Wartung & Support

### 🔧 **Regelmäßige Wartung**
- Kalibrierung alle 6 Monate
- Software-Updates monatlich
- Hardware-Inspektion vierteljährlich
- Akku-Wartung nach Bedarf

### 📞 **Support-Kontakte**
- Hardware-Probleme: Lokaler Elektronik-Service
- Software-Updates: Git Repository
- Kalibrierung: Eich-Service oder DIY

---

## Status: BEREIT FÜR BESCHAFFUNG ✅

Das System ist **softwareseitig vollständig vorbereitet** und kann nach Hardware-Beschaffung sofort implementiert werden!

**Nächste Schritte:**
1. 🛒 Hardware bestellen (Budget: €500-700)
2. 📦 Komponenten testen
3. 🔧 Mechanische Integration
4. ✅ Software auf Pi5 installieren
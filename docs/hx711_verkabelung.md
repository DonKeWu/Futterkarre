# 🔌 HX711 Wägezellen-Verkabelung für Futterkarre 2.0

## 📍 **Pin-Übersicht Raspberry Pi 5**

### **GPIO-Header (40-polig):**
```
        3V3  (1) (2)  5V    ← VCC für HX711-Module
       GPIO2 (3) (4)  5V    ← VCC für HX711-Module  
       GPIO3 (5) (6)  GND   ← GND für HX711_1
       GPIO4 (7) (8)  GPIO14
         GND (9) (10) GPIO15 ← GND für HX711_2
      GPIO17 (11)(12) GPIO18
      GPIO27 (13)(14) GND   ← GND für HX711_3
      GPIO22 (15)(16) GPIO23
        3V3 (17)(18) GPIO24
      GPIO10 (19)(20) GND   ← GND für HX711_4
       GPIO9 (21)(22) GPIO25
      GPIO11 (23)(24) GPIO8
         GND (25)(26) GPIO7
       GPIO0 (27)(28) GPIO1
   →  GPIO5 (29)(30) GND
   →  GPIO6 (31)(32) GPIO12
   → GPIO13 (33)(34) GND
   → GPIO19 (35)(36) GPIO16 ←
   → GPIO26 (37)(38) GPIO20 ←
         GND (39)(40) GPIO21 ←
```

## 🔌 **Verkabelungsplan für 4x HX711-Module (Option 1 - EMPFOHLEN)**

### **Wägezelle 1 - Vorne Links (VL):**
```
HX711-Modul 1:
├── VCC → Raspberry Pi Pin 2 (5V)
├── GND → Raspberry Pi Pin 6 (GND)
├── DT  → Raspberry Pi Pin 29 (GPIO 5)
└── SCK → Raspberry Pi Pin 31 (GPIO 6)

Wägezelle → HX711:
├── E+ (Excitation+) → VCC des HX711
├── E- (Excitation-) → GND des HX711  
├── A+ (Signal+)     → A+ des HX711
└── A- (Signal-)     → A- des HX711
```

### **Wägezelle 2 - Vorne Rechts (VR):**
```
HX711-Modul 2:
├── VCC → Raspberry Pi Pin 4 (5V)
├── GND → Raspberry Pi Pin 9 (GND)
├── DT  → Raspberry Pi Pin 33 (GPIO 13)
└── SCK → Raspberry Pi Pin 35 (GPIO 19)
```

### **Wägezelle 3 - Hinten Links (HL):**
```
HX711-Modul 3:
├── VCC → Raspberry Pi Pin 2 (5V) [parallel zu Modul 1]
├── GND → Raspberry Pi Pin 14 (GND)
├── DT  → Raspberry Pi Pin 37 (GPIO 26)
└── SCK → Raspberry Pi Pin 40 (GPIO 21)
```

### **Wägezelle 4 - Hinten Rechts (HR):**
```
HX711-Modul 4:
├── VCC → Raspberry Pi Pin 4 (5V) [parallel zu Modul 2]
├── GND → Raspberry Pi Pin 20 (GND)
├── DT  → Raspberry Pi Pin 38 (GPIO 20)
└── SCK → Raspberry Pi Pin 36 (GPIO 16)
```

## ⚡ **Stromversorgung**

### **5V-Verteilung:**
- **Pin 2 (5V):** HX711-Module 1 + 3 (Vorne/Hinten Links)
- **Pin 4 (5V):** HX711-Module 2 + 4 (Vorne/Hinten Rechts)
- **Maximaler Strom:** ~100mA pro HX711 = 400mA gesamt
- **Raspberry Pi 5 kann bis zu 1.6A über 5V-Pins liefern → ausreichend!**

### **GND-Verteilung:**
- **Pin 6:** HX711-Modul 1 (Vorne Links)
- **Pin 9:** HX711-Modul 2 (Vorne Rechts)  
- **Pin 14:** HX711-Modul 3 (Hinten Links)
- **Pin 20:** HX711-Modul 4 (Hinten Rechts)

## 🧰 **Benötigte Hardware**

### **HX711-Module (4x):**
- **Typ:** HX711 24-Bit ADC Wägezellen-Verstärker
- **Eingangsspannung:** 2.7V - 5.5V (5V empfohlen)
- **Auflösung:** 24-Bit (8.388.608 Stufen)
- **Abtastrate:** 10Hz oder 80Hz (einstellbar)
- **Interface:** 2-Draht (DT + SCK)

### **Wägezellen (4x):**
- **Typ:** Aluminium-Biegebalken oder S-Type Load Cells
- **Kapazität:** 50kg - 200kg je nach Anwendung
- **Ausgangssignal:** 2mV/V (typisch)
- **Eingangswiderstand:** 350Ω - 1000Ω
- **Schutzart:** IP65+ für Stallumgebung

### **Verkabelung:**
- **Verbindungskabel:** 4-adriges geschirmtes Kabel (für jede Wägezelle)
- **Länge:** Max. 10m zwischen Wägezelle und HX711
- **Jumperkabel:** Male-Female für RPi-Verbindung
- **Schraubklemmen:** Für sichere Wägezellen-Anschlüsse

## 🔧 **Montage-Hinweise**

### **Mechanischer Aufbau:**
```
🚜 Futterkarre (Draufsicht):
     VL ---- VR
     |        |
     |   🎯   |  ← Schwerpunkt
     |        |  
     HL ---- HR

VL = Vorne Links  (GPIO 5/6)
VR = Vorne Rechts (GPIO 13/19)
HL = Hinten Links (GPIO 26/21)  
HR = Hinten Rechts (GPIO 20/16)
```

### **Wägezellen-Positionierung:**
- **Symmetrische Montage:** Alle 4 Ecken des Karren-Rahmens
- **Schutz vor Seitenkräften:** Pendelaufhängung oder Führungen
- **Höhenausgleich:** Justierbare Befestigung für Nullpunkt-Ausgleich
- **Überlastschutz:** Mechanische Anschläge bei > 150% Nennlast

## 📝 **Kalibrierungsprozedur**

### **1. Mechanische Justierung:**
```bash
# 1. Karren leer auf alle 4 Wägezellen stellen
# 2. Prüfen ob alle Zellen gleichmäßig belastet sind
# 3. Mechanische Justierung falls nötig
```

### **2. Software-Kalibrierung:**
```python
# In Python (interactive_py_converter.py):
from hardware.hx711_real import kalibriere_sensor

# Nullpunkt setzen (Karren leer):
for i in range(4):
    kalibriere_sensor(i, 0)

# Bekanntes Gewicht auflegen (z.B. 20kg):
kalibriere_sensor(0, 20.0)  # Vorne Links
# ... für alle 4 Sensoren wiederholen
```

### **3. Genauigkeitstest:**
```python
from hardware.hx711_real import lese_einzelzellwerte_hx711

# Test mit verschiedenen Gewichten:
print("Werte pro Zelle:", lese_einzelzellwerte_hx711())
print("Gesamtgewicht:", sum(lese_einzelzellwerte_hx711()))
```

## ⚠️ **Wichtige Hinweise**

### **Elektrische Sicherheit:**
- **ESD-Schutz:** HX711-Module sind ESD-empfindlich
- **Überspannung:** Niemals > 5.5V an VCC anlegen
- **Kurzschluss:** GND und VCC nicht vertauschen
- **Abschirmung:** Geschirmte Kabel für Wägezellen verwenden

### **Mechanische Stabilität:**
- **Vibrationen:** Können Messwerte verfälschen
- **Temperatur:** HX711 hat Temperaturdrift (~3ppm/°C)
- **Feuchtigkeit:** IP65-Schutz für Außeneinsatz erforderlich
- **Überlast:** Kann Wägezellen dauerhaft beschädigen

### **Software-Optimierung:**
- **Sampling-Rate:** 10Hz für stabile Messungen
- **Mittelwertbildung:** 3-10 Messungen pro Wert
- **Filterung:** Gleitender Mittelwert gegen Rauschen
- **Kalibrierung:** Regelmäßig mit bekannten Gewichten

## 🚀 **Test-Kommandos**

### **GPIO-Test:**
```python
# GPIO-Pins testen:
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# Alle SCK-Pins als Output testen:
for pin in [6, 19, 21, 16]:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    print(f"GPIO {pin}: HIGH")
```

### **HX711-Kommunikation testen:**
```python
from hardware.hx711_real import lese_einzelzellwerte_hx711

try:
    werte = lese_einzelzellwerte_hx711()
    print(f"✅ Alle 4 HX711 erreichbar: {werte}")
except Exception as e:
    print(f"❌ HX711-Fehler: {e}")
```

---

**🎯 Nächste Schritte:**
1. ✅ Pin-Plan überprüfen
2. 🛒 Hardware bestellen (4x HX711 + 4x Wägezellen)
3. 🔧 Breadboard-Prototyp aufbauen  
4. 📝 Kalibrierung durchführen
5. 🚜 In Karren-Rahmen integrieren
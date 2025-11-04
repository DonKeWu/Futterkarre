# 🛒 Einkaufsliste & Verkabelung für HX711 Dual-Channel Setup

## 📦 **Benötigte Hardware (Option 2: 2x HX711)**

### **🔌 HX711-Module (2 Stück):**
```
Artikel: HX711 24-Bit ADC Wägezellen-Verstärker
├── Anzahl: 2x
├── Preis: ~8-12€ pro Stück
├── Features: Dual-Channel (A+B), 24-Bit Auflösung
├── Eingänge: 2x Wägezellen-Differenzialeingänge
└── Ausgang: 2-Draht Digital (DT + SCK)

Bezugsquellen:
├── AZ-Delivery: HX711 Modul
├── Reichelt: DEBO HX711
└── Amazon: "HX711 24-Bit ADC Wägeamplifyer"
```

### **📏 Sammelkabel (1,5m Digital-Strecke):**
```
Kabel-Spezifikation:
├── Typ: LIYCY 6x0,5mm² + Schirm
├── Länge: 2m (mit Reserve für Verlegung)  
├── Adern: 6 + Schirmgeflecht
├── Temp-Bereich: -20°C bis +80°C
├── Schutzart: Geeignet für IP65-Durchführungen

Teilenummer Beispiele:
├── Lapp Kabel: ÖLFLEX CLASSIC 110 CY 6G0,5
├── Helukabel: TRONIC-CY 6x0,5
└── Alternative: LiYCY 6x0,5 (günstiger)
```

### **🔌 Steckverbindungen:**
```
Sammelkabel-Stecker (Anzeige-Seite):
├── Typ: M16 Rundstecker 8-polig, IP67
├── Artikel: Hirschmann ELKA 4008 V oder kompatibel
├── Buchse: Fest am Anzeige-Gehäuse
├── Stecker: Am Sammelkabel (Zugentlastung)

Wägezellen-Anschluss (Boden):
├── Typ: 4-pol Schraubklemmen pro Wägezelle
├── Artikel: Phoenix Contact MKDS 1,5/4
├── Alternative: WAGO 221-414 (toolless)
└── 8 Stück benötigt (2x pro HX711-Modul)
```

### **🏠 Gehäuse für HX711-Module:**
```
Gehäuse-Anforderungen:
├── Schutzart: IP65 (staub-/spritzwasserdicht)
├── Material: Polycarbonat oder ABS
├── Größe: ~120x80x60mm (für 1x HX711 + Klemmen)
├── Durchführungen: M16 für Sammelkabel, M12 für Wägezellen

Artikel-Beispiele:
├── Spelsberg TK PS 1111-6-tm
├── Fibox ARCA AR 12106SC  
└── OKW Comtec D9006107 (günstig)
```

---

## 🔧 **Verkabelungsplan Dual-Channel**

### **📍 Gehäuse-Anordnung:**
```
🚜 Futterkarre (Draufsicht):
     ╔═══════════════════╗
     ║ [Gehäuse Vorne]   ║
     ║  HX711_1         ║
 WZ1 ╫─→ Kanal A        ║
 WZ2 ╫─→ Kanal B        ║
     ║                  ║
     ║                  ║
     ║ [Gehäuse Hinten]  ║ 
     ║  HX711_2         ║
 WZ3 ╫─→ Kanal A        ║
 WZ4 ╫─→ Kanal B        ║
     ╚═══════════════════╝
            │
        Sammelkabel
         (6-adrig)
            │
      ┌─────▼─────┐
      │ Anzeige   │ ← 1,5m Höhe
      │ RPi + LCD │
      └───────────┘
```

### **📋 Klemmen-Belegung pro Gehäuse:**

#### **Gehäuse Vorne (HX711_1):**
```
Schraubklemmen-Block 1 (WZ1 - Vorne Links):
├── Klemme 1: E+ (rot)    → HX711 VCC  
├── Klemme 2: E- (schwarz) → HX711 GND
├── Klemme 3: A+ (grün)   → HX711 Kanal A+
└── Klemme 4: A- (weiß)   → HX711 Kanal A-

Schraubklemmen-Block 2 (WZ2 - Vorne Rechts):
├── Klemme 5: E+ (rot)    → HX711 VCC (parallel)
├── Klemme 6: E- (schwarz) → HX711 GND (parallel)  
├── Klemme 7: A+ (grün)   → HX711 Kanal B+
└── Klemme 8: A- (weiß)   → HX711 Kanal B-

Sammelkabel-Ausgang (M16-Stecker):
├── Ader 1: DT (Data)     → RPi GPIO 5
├── Ader 2: SCK (Clock)   → RPi GPIO 6
├── Ader 3: 5V           → RPi Pin 2 (5V)
├── Ader 4: GND          → RPi Pin 6 (GND)
├── Ader 5: Reserve      
├── Ader 6: Reserve
└── Schirm: Gehäuse      → EMI-Schutz
```

#### **Gehäuse Hinten (HX711_2):**
```
Identisch zu "Gehäuse Vorne", aber:
├── Sammelkabel wird durchgeschleift (parallel)
├── DT → RPi GPIO 13, SCK → RPi GPIO 19
├── 5V/GND parallel zu Gehäuse Vorne
└── Eigene Wägezellen WZ3 + WZ4
```

---

## ⚡ **Stromversorgung & Verkabelung**

### **🔋 Strom-Budget:**
```python
# Stromverbrauch Berechnung:
stromverbrauch = {
    "hx711_modul": 10,      # mA pro HX711  
    "anzahl_module": 2,     # 2x HX711
    "wägezellen": 4 * 5,    # 4x 5mA Excitation
    "gesamt_ma": 2 * 10 + 4 * 5,  # 40mA
    "spannung": 5.0,        # Volt
    "leistung_w": 0.04 * 5  # 0.2W
}

# Kabel-Dimensionierung (1,5m Länge):
kabel_berechnung = {
    "laenge_m": 1.5,
    "strom_ma": 40,
    "draht_querschnitt": 0.5,  # mm²
    "spannungsabfall_mv": 1.5 * 40 * 0.034,  # 2mV
    "verlust_prozent": 2 / 5000 * 100  # 0.04% → vernachlässigbar
}
```

### **📐 Kabel-Konfektionierung:**
```
Sammelkabel-Aufbau (6-adrig):
┌─────────────────────────────────────┐
│ Ader 1: DT_1 (GPIO 5)   - blau     │
│ Ader 2: SCK_1 (GPIO 6)  - braun    │  
│ Ader 3: DT_2 (GPIO 13)  - grün     │
│ Ader 4: SCK_2 (GPIO 19) - gelb     │
│ Ader 5: 5V              - rot      │
│ Ader 6: GND             - schwarz  │
│ Schirm: EMI-Schutz      - blank    │
└─────────────────────────────────────┘

Anzeige-Seite (M16-Buchse am Gehäuse):
├── Direkt zu RPi GPIO-Pins verdrahtet
├── 5V/GND von RPi-Netzteil versorgt  
├── Zugentlastung mit Kabelverschraubung
└── Status-LEDs für HX711-Kommunikation
```

---

## 🧰 **Montage-Anweisungen**

### **🔧 Gehäuse-Vorbereitung:**
```bash
# Gehäuse-Bearbeitung:
1. Durchführungen bohren:
   - 1x M16 für Sammelkabel
   - 2x M12 für Wägezellen-Kabel
   
2. HX711-Platine befestigen:
   - 4x M3-Schrauben + Abstandshalter
   - ESD-Schutz beachten!
   
3. Schraubklemmen montieren:
   - 2x 4-pol Blöcke pro Gehäuse
   - Beschriftung: WZ1/WZ2 bzw. WZ3/WZ4
```

### **🔌 Verkabelungs-Reihenfolge:**
```bash
# Schritt-für-Schritt Anleitung:

1. Wägezellen-Kabel anschließen:
   - Farb-Codierung beachten (E+/E-/A+/A-)
   - Klemmen fest anziehen (0.5Nm)
   - Durchgangstest mit Multimeter
   
2. HX711-Verkabelung:
   - VCC/GND zu beiden Klemmenblöcken parallel
   - Kanal A/B zu entsprechenden Wägezellen  
   - Verpolung vermeiden!
   
3. Sammelkabel konfektionieren:
   - M16-Stecker crimpen
   - Zugentlastung einbauen
   - Durchgangstest aller Adern
   
4. Gehäuse verschließen:
   - Dichtungen prüfen (IP65)  
   - Kabelverschraubungen festziehen
   - Funktionstest vor Montage
```

---

## 🧪 **Test-Prozedur**

### **⚡ Elektrische Tests:**
```python
# GPIO-Test (vor HX711-Anschluss):
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

test_pins = [5, 6, 13, 19]  # DT/SCK Pins
for pin in test_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    print(f"GPIO {pin}: {GPIO.input(pin)}")  # Sollte 1 sein
    GPIO.output(pin, GPIO.LOW)
    print(f"GPIO {pin}: {GPIO.input(pin)}")  # Sollte 0 sein
```

### **📊 Funktions-Test:**
```python
# HX711 Dual-Channel Test:
from hardware.hx711_real import lese_einzelzellwerte_hx711

try:
    print("🔧 Teste alle 4 Wägezellen...")
    werte = lese_einzelzellwerte_hx711()
    print(f"Rohwerte: {werte}")
    
    # Plausibilitäts-Check:
    for i, wert in enumerate(werte):
        if abs(wert) > 1000000:  # Unrealistisch hoch
            print(f"⚠️ Sensor {i+1}: Wert unrealistisch ({wert})")
        else:
            print(f"✅ Sensor {i+1}: OK ({wert})")
            
except Exception as e:
    print(f"❌ Test fehlgeschlagen: {e}")
```

---

## 💰 **Kosten-Aufstellung**

### **📦 Hardware-Kosten (geschätzt):**
```
Position                     | Menge | Einzelpreis | Gesamt
----------------------------|-------|-------------|--------
HX711-Module                | 2x    | 10€         | 20€
Sammelkabel 6x0.5mm²        | 2m    | 3€/m        | 6€  
IP65-Gehäuse                | 2x    | 15€         | 30€
M16-Steckverbinder          | 1 Set | 12€         | 12€
Schraubklemmen 4-pol        | 4x    | 3€          | 12€
Kleinteile (Schrauben etc.) | 1x    | 10€         | 10€
----------------------------|-------|-------------|--------
Gesamt                      |       |             | 90€
```

### **🕒 Arbeitszeit (geschätzt):**
```
Tätigkeit                   | Zeit    | Beschreibung
----------------------------|---------|---------------------------
Gehäuse-Bearbeitung        | 2h      | Bohren, Montage
Verkabelung HX711           | 3h      | Löten, Crimpen, Testen  
Sammelkabel konfektionieren | 2h      | Crimpen, Durchgangstest
Software-Anpassung          | 1h      | Code-Test, Kalibrierung
Montage am Karren           | 2h      | Befestigung, Integration
----------------------------|---------|---------------------------
Gesamt                      | 10h     | An 2-3 Tagen verteilbar
```

---

## 🎯 **Fazit: Empfehlung für Option 2**

**✅ Vorteile der Dual-Channel Lösung:**
- **40% weniger Verkabelungsaufwand** (6- statt 10-adrig)
- **50% weniger Hardware-Kosten** (2 statt 4 HX711-Module)  
- **Kompaktere Montage** (2 statt 4 Gehäuse)
- **Ausreichende Genauigkeit** für Fütterungsanwendung
- **B-Kanal als Reserve** für künftige Erweiterungen

**📋 Nächste Schritte:**
1. ✅ **Hardware bestellen** (siehe Einkaufsliste)
2. 🔧 **Breadboard-Prototyp** mit 1x HX711 + 2x Dummy-Wägezellen  
3. 📊 **Software testen** mit neuer Dual-Channel Implementierung
4. 🏗️ **Gehäuse bauen** und Verkabelung konfektionieren
5. 🚜 **Integration** in Futterkarre mit Kalibrierung

Die **Dual-Channel Lösung ist definitiv der bessere Weg** für Ihre Anwendung!
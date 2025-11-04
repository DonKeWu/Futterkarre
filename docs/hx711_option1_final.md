# 🛒 Einkaufsliste HX711 - Option 1: 4x separate Module (EMPFOHLEN)

## 🎯 **Warum Option 1 (4x separate HX711) die bessere Wahl ist:**

```
✅ Alle Wägezellen gleichwertig behandelt
✅ Keine Verstärkungsunterschiede  
✅ Einfache Fehlerdiagnose
✅ Jedes Modul einzeln austauschbar
✅ Zukunftssicher für präzise Anwendungen
✅ Professioneller Aufbau
```

**💰 Mehrkosten vs. Dual-Channel: Nur 20€ für deutlich mehr Zuverlässigkeit!**

---

## 📦 **Hardware-Liste (4x HX711 Setup)**

### **🔌 HX711-Module (4 Stück):**
```
Artikel: HX711 24-Bit ADC Wägezellen-Verstärker
├── Anzahl: 4x (je 1 pro Wägezelle)
├── Preis: ~8-12€ pro Stück = 32-48€ gesamt
├── Features: 24-Bit Auflösung, 128x Verstärkung
├── Eingänge: 1x Wägezellen-Differenzialeingang pro Modul
└── Ausgang: 2-Draht Digital (DT + SCK)

Bezugsquellen:
├── AZ-Delivery: HX711 Modul (~9€/Stück)
├── Reichelt: DEBO HX711 (~10€/Stück)
└── Amazon: "HX711 24-Bit ADC" Set 5x für ~35€
```

### **📏 Sammelkabel (1,5m Digital-Strecke):**
```
Kabel-Spezifikation:
├── Typ: LIYCY 10x0,5mm² + Schirm
├── Länge: 2m (mit Reserve für Verlegung)  
├── Adern: 8x Signal + 2x Stromversorgung
├── Temp-Bereich: -20°C bis +80°C
├── Schutzart: Geeignet für IP65-Durchführungen

Konkrete Artikel:
├── Lapp Kabel: ÖLFLEX CLASSIC 110 CY 10G0,5 (~8€/m)
├── Helukabel: TRONIC-CY 10x0,5 (~6€/m)
└── Alternative: LiYCY 10x0,5 (~4€/m, günstiger)
```

### **🔌 Steckverbindungen:**
```
Sammelkabel-Stecker (Anzeige-Seite):
├── Typ: M20 Rundstecker 12-polig, IP67
├── Artikel: Hirschmann ELKA 4012 V oder kompatibel
├── Buchse: Fest am Anzeige-Gehäuse
├── Stecker: Am Sammelkabel (Zugentlastung)

Wägezellen-Anschluss (Boden):
├── Typ: 4-pol Schraubklemmen pro Wägezelle
├── Artikel: Phoenix Contact MKDS 1,5/4
├── Alternative: WAGO 221-414 (toolless)
└── 4 Stück benötigt (1x pro HX711-Modul)
```

### **🏠 Gehäuse für HX711-Module:**
```
Gehäuse-Anforderungen:
├── Schutzart: IP65 (staub-/spritzwasserdicht)
├── Material: Polycarbonat oder ABS
├── Größe: ~100x80x50mm (für 1x HX711 + Klemmen)
├── Durchführungen: M12 für Wägezelle, M16 für Sammelkabel

Empfohlene Artikel:
├── Spelsberg TK PS 1008-6-tm (~12€/Stück)
├── Fibox ARCA AR 10805SC (~15€/Stück)
└── OKW Comtec D9006107 (~8€/Stück, günstig)
```

---

## 🔧 **Verkabelungsplan (4x separate Module)**

### **📍 Pin-Zuordnung Raspberry Pi 5:**
```
Wägezelle 1 (Vorne Links):
├── HX711_1: DT → GPIO 5, SCK → GPIO 6
├── VCC → Pin 2 (5V), GND → Pin 6 (GND)

Wägezelle 2 (Vorne Rechts):  
├── HX711_2: DT → GPIO 13, SCK → GPIO 19
├── VCC → Pin 4 (5V), GND → Pin 9 (GND)

Wägezelle 3 (Hinten Links):
├── HX711_3: DT → GPIO 26, SCK → GPIO 21  
├── VCC → Pin 2 (5V), GND → Pin 14 (GND)

Wägezelle 4 (Hinten Rechts):
├── HX711_4: DT → GPIO 20, SCK → GPIO 16
├── VCC → Pin 4 (5V), GND → Pin 20 (GND)
```

### **📋 Sammelkabel-Belegung (10-adrig):**
```
LIYCY 10x0,5mm² Sammelkabel:
├── Ader 1: DT_1 (GPIO 5)    - blau
├── Ader 2: SCK_1 (GPIO 6)   - braun
├── Ader 3: DT_2 (GPIO 13)   - grün  
├── Ader 4: SCK_2 (GPIO 19)  - gelb
├── Ader 5: DT_3 (GPIO 26)   - grau
├── Ader 6: SCK_3 (GPIO 21)  - rosa
├── Ader 7: DT_4 (GPIO 20)   - violett
├── Ader 8: SCK_4 (GPIO 16)  - türkis
├── Ader 9: 5V               - rot
├── Ader 10: GND             - schwarz
└── Schirm: EMI-Schutz       - blank
```

### **🏗️ Mechanischer Aufbau:**
```
🚜 Futterkarre (Draufsicht):
     ╔═══════════════════╗
     ║ [HX711_1] [HX711_2] ║ ← Vorne
 WZ1 ╫─→ Modul 1        ║
 WZ2 ╫─→       Modul 2  ║
     ║                  ║
     ║ [HX711_3] [HX711_4] ║ ← Hinten
 WZ3 ╫─→ Modul 3        ║
 WZ4 ╫─→       Modul 4  ║
     ╚═══════════════════╝
            │
       Sammelkabel
        (10-adrig)
            │
      ┌─────▼─────┐
      │ Anzeige   │ ← 1,5m Höhe
      │ RPi + LCD │
      └───────────┘
```

---

## 💰 **Kosten-Aufstellung (4x HX711)**

### **📦 Hardware-Kosten:**
```
Position                     | Menge | Einzelpreis | Gesamt
----------------------------|-------|-------------|--------
HX711-Module                | 4x    | 10€         | 40€
Sammelkabel 10x0.5mm²       | 2m    | 4€/m        | 8€  
IP65-Gehäuse klein          | 4x    | 12€         | 48€
M20-Steckverbinder          | 1 Set | 15€         | 15€
Schraubklemmen 4-pol        | 4x    | 3€          | 12€
Kleinteile (Schrauben etc.) | 1x    | 15€         | 15€
----------------------------|-------|-------------|--------
Gesamt                      |       |             | 138€
```

### **🔄 Vergleich zu Dual-Channel:**
```
Option 1 (4x HX711):  138€
Option 2 (2x HX711):   90€
Unterschied:           48€

Für 48€ mehr:
✅ Keine Verstärkungsunterschiede
✅ Symmetrische Behandlung aller Wägezellen
✅ Einfachere Wartung und Diagnose
✅ Professionellerer Aufbau
✅ Zukunftssicherheit
```

---

## 🛒 **Konkrete Bestell-Links (Option 1)**

### **🚀 Amazon Prime (1-2 Tage):**
```
HX711-Module (5er-Set für Reserve):
├── Suchbegriff: "HX711 5er Set 24-Bit ADC"
├── Preis: ~35-45€ für 5 Stück
├── Vorteil: 1 Reserve-Modul für Reparaturen

Sammelkabel:
├── Suchbegriff: "LiYCY Steuerleitung 10x0,5 geschirmt"
├── Alternative: "ÖLFLEX CLASSIC 110 CY 10G0,5"
├── Preis: ~25€ für 5m Rolle

Gehäuse-Set:
├── Suchbegriff: "IP65 Gehäuse Set Kunststoff klein"
├── Preis: ~40-60€ für 5er-Set
├── Größe: 100x80x50mm oder ähnlich
```

### **💰 Günstige Alternative (3-5 Tage):**
```
HX711: AZ-Delivery einzeln bestellen
├── 4x https://www.az-delivery.de/products/hx711-wageamplifyer
├── 4x 8,99€ = 35,96€

Kabel: Reichelt Meterware
├── LIYCY 10x0,5mm² Steuerleitung
├── 2m für ~8-12€

Gehäuse: Conrad Einzelbestellung
├── 4x Spelsberg TK PS oder OKW
├── ~12€ pro Stück = 48€
```

---

## ✅ **Warum Option 1 die richtige Entscheidung ist:**

### **🔬 Technische Vorteile:**
```
1. Einheitliche Verstärkung:
   ├── Alle 4 Kanäle: 128x Verstärkung
   ├── Gleiche Auflösung: ~0.76g pro Schritt
   ├── Symmetrisches Verhalten
   └── Vorhersagbare Kalibrierung

2. Unabhängige Module:
   ├── Einzelne Sensoren austauschbar
   ├── Defekte isoliert identifizierbar  
   ├── Separate Kalibrierung möglich
   └── Einfache Wartung

3. Saubere Software:
   ├── Keine Channel-Switching-Logik
   ├── Weniger Fehlerquellen
   ├── Bessere Debugging-Möglichkeiten
   └── Klarere Code-Struktur
```

### **🏆 Praktische Vorteile:**
```
1. Zuverlässigkeit:
   ├── Kein asymmetrisches Verhalten
   ├── Weniger softwarebedingte Probleme
   ├── Robustere Langzeit-Stabilität
   └── Professioneller Standard

2. Wartungsfreundlichkeit:
   ├── Einzelne Module schnell tauschbar
   ├── Klare Fehlerzuordnung möglich
   ├── Ersatzteile einfach verfügbar
   └── Reduzierte Ausfallzeiten

3. Zukunftssicherheit:
   ├── Erweiterung auf präzisere Anwendungen
   ├── Kompatibel mit Standard-Libraries
   ├── Bewährtes Design-Pattern
   └── Langzeit-Support gesichert
```

---

## 🎯 **Empfehlung: Option 1 bestellen!**

**Die zusätzlichen 48€ sind eine Investition in:**
- ✅ **Zuverlässigkeit** über Jahre hinweg
- ✅ **Einfache Wartung** und Problemlösung  
- ✅ **Professioneller Standard** ohne Kompromisse
- ✅ **Zukunftssicherheit** für erweiterte Anwendungen

**Ihre technische Intuition bezüglich der Verstärkungsunterschiede war absolut richtig!** 👍
# 🔌 ESP8266 Arduino-Sketch Flash-Anleitung

## 📋 **Übersicht**

Unabhängige Anleitung zum Flashen des **ESP8266 NodeMCU** mit dem Futterkarre Wireless-Waage Sketch, **ohne** die Pi5-Python-Umgebung zu beeinträchtigen.

## 🛠️ **Hardware-Anforderungen**

- **ESP8266 NodeMCU v3** (oder kompatibel)
- **4x HX711** 24-Bit ADC Module
- **4x Wägezellen** (Load Cells)
- **18650 Akku + TP4056 Ladeplatine**
- **Breadboard/Lötplatine** für Verkabelung
- **USB-Kabel** (Micro-USB für NodeMCU)

## 💻 **Software-Setup**

### **1. Arduino IDE installieren**

```bash
# Ubuntu/Debian:
sudo snap install arduino

# Oder Download von: https://www.arduino.cc/en/software
```

### **2. ESP8266 Board-Support hinzufügen**

1. **Arduino IDE starten**
2. **Datei → Voreinstellungen**
3. **Zusätzliche Boardverwalter-URLs:**
   ```
   http://arduino.esp8266.com/stable/package_esp8266com_index.json
   ```
4. **Tools → Board → Boardverwalter**
5. Suche: **"esp8266"**
6. **ESP8266 Community** installieren (Version 3.x)

### **3. Benötigte Libraries installieren**

**Tools → Bibliotheken verwalten**, dann installieren:

- ✅ **HX711** (von Bogdan Necula)
- ✅ **ArduinoJson** (Version 6.x)
- ✅ **WebSockets** (von Markus Sattler)

## 🔧 **Sketch-Konfiguration**

### **1. Sketch öffnen**

```bash
# Navigiere zum Sketch:
cd /home/daniel/Dokumente/HOF/Futterwagen/Python/Futterkarre/wireless/esp8266/

# Öffne in Arduino IDE:
arduino futterkarre_wireless_waage_esp8266.ino
```

### **2. WiFi-Einstellungen anpassen**

**Im Sketch (Zeilen 30-32):**
```cpp
const char* WIFI_SSID = "DEIN_WIFI_NAME";      // ← ANPASSEN!
const char* WIFI_PASSWORD = "DEIN_WIFI_PASSWORT";   // ← ANPASSEN!
```

### **3. Hardware-Pins prüfen**

**Standardmäßig konfiguriert für NodeMCU v3:**
```cpp
// HX711 Pin-Mapping:
HX711_1 (vorne-links):  CLK=D1(GPIO5),  DT=D2(GPIO4)
HX711_2 (vorne-rechts): CLK=D3(GPIO0),  DT=D4(GPIO2)
HX711_3 (hinten-links): CLK=D5(GPIO14), DT=D6(GPIO12)
HX711_4 (hinten-rechts):CLK=D7(GPIO13), DT=D8(GPIO15)

// Status-LEDs:
Power LED (grün):  D0 (GPIO16)
WiFi LED (blau):   Built-in (GPIO2)
Akku-Monitor:      A0 (ADC)
```

## ⚡ **Flash-Prozess**

### **1. ESP8266 vorbereiten**

1. **ESP8266 NodeMCU** per USB verbinden
2. **Board konfigurieren:**
   - **Tools → Board: "NodeMCU 1.0 (ESP-12E Module)"**
   - **Tools → Port:** `/dev/ttyUSB0` (oder `/dev/ttyACM0`)
   - **Tools → Upload Speed: "115200"**
   - **Tools → CPU Frequency: "80 MHz"**
   - **Tools → Flash Size: "4MB (FS:2MB OTA:~1019KB)"**

### **2. Sketch kompilieren & flashen**

```bash
# In Arduino IDE:
1. Sketch → Überprüfen/Kompilieren  ✅
2. Sketch → Hochladen              🚀
```

**Erwartete Ausgabe:**
```
Kompilierung... OK
Hochladen... OK
Schwer verfügbaren Speicher: 315392 Bytes
```

### **3. Serial Monitor testen**

1. **Tools → Serieller Monitor** (115200 Baud)
2. **ESP8266 Reset-Button** drücken

**Erwartete Ausgabe:**
```
=================================
🚀 Futterkarre Wireless Waage
   ESP8266 NodeMCU Version
=================================
🔧 GPIO initialisieren... OK
⚖️  HX711 Waagen initialisieren... OK
📡 WiFi verbinden... OK
   IP: 192.168.1.xxx
   RSSI: -45 dBm
🔌 WebSocket-Server starten... OK (Port 81)
✅ System bereit!
```

## 🧪 **Funktions-Test**

### **1. WiFi-Verbindung prüfen**

```bash
# Von einem anderen Gerät im gleichen Netzwerk:
ping 192.168.1.xxx  # IP aus Serial Monitor
```

### **2. WebSocket-Kommunikation testen**

**Python-Test-Script (optional):**
```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"📨 Empfangen: {data}")

# ESP8266 IP aus Serial Monitor verwenden:
ws = websocket.WebSocketApp("ws://192.168.1.xxx:81",
                          on_message=on_message)
ws.run_forever()
```

### **3. Gewichtsmessung testen**

1. **Gewicht auf Waage legen**
2. **Serial Monitor beobachten**
3. **JSON-Messages** sollten erscheinen:
   ```json
   {
     "type": "weight_data",
     "total_kg": 5.24,
     "corners": [1.31, 1.28, 1.33, 1.32],
     "battery_v": 4.1,
     "wifi_rssi": -45
   }
   ```

## 🔍 **Troubleshooting**

### **Kompilierungs-Fehler:**
```bash
❌ 'WebSocketsServer' was not declared
→ Library "WebSockets" installieren

❌ 'HX711' was not declared  
→ Library "HX711" installieren

❌ Board esp8266:esp8266:nodemcuv2 not found
→ ESP8266 Board-Support installieren
```

### **Upload-Fehler:**
```bash
❌ Failed to connect to ESP8266
→ Richtigen Port wählen (/dev/ttyUSB0)
→ ESP8266 Reset-Button drücken während Upload

❌ Access denied /dev/ttyUSB0
→ sudo usermod -a -G dialout $USER
→ Terminal neustarten
```

### **Runtime-Fehler:**
```bash
❌ WiFi-Verbindung fehlgeschlagen
→ SSID/Passwort in Sketch prüfen
→ WiFi-Frequenz: 2.4GHz (nicht 5GHz!)

❌ HX711 nicht bereit
→ Verkabelung prüfen (CLK/DT Pins)
→ Stromversorgung: 5V für HX711
```

## 📊 **Pi5-Integration**

Nach erfolgreichem Flash:

1. **ESP8266 IP-Adresse notieren** (aus Serial Monitor)
2. **In Pi5 Python-Code konfigurieren:**
   ```python
   # wireless/wireless_weight_manager.py
   ESP8266_IP = "192.168.1.xxx"  # ← Deine ESP8266 IP
   ```

## 🔋 **Power-Management**

### **Akku-Überwachung:**
- **Grüne LED:** System läuft normal
- **Blaue LED:** WiFi verbunden  
- **Rote LED (blinkt):** Niedrige Spannung
- **Deep Sleep:** Automatisch bei kritischer Spannung

### **Betriebsdauer:**
- **Aktiv:** ~8-12 Stunden (je nach Akku)
- **Deep Sleep:** Mehrere Tage
- **Laden:** TP4056 Ladeplatine (USB-C/Micro-USB)

## ✅ **Erfolgreiche Installation**

Du hast erfolgreich den ESP8266 geflasht wenn:

- ✅ **Kompilierung** ohne Fehler
- ✅ **Upload** erfolgreich (315KB+ verwendet)  
- ✅ **Serial Monitor** zeigt System-Start
- ✅ **WiFi-Verbindung** hergestellt
- ✅ **WebSocket-Server** läuft (Port 81)
- ✅ **Gewichtsdaten** werden gesendet
- ✅ **Status-LEDs** funktionieren

**Der ESP8266 ist jetzt bereit für die Integration mit dem Pi5-Futterkarre-System!** 🎉

---

## 📎 **Wichtige Dateien**

- **Sketch:** `wireless/esp8266/futterkarre_wireless_waage_esp8266.ino`
- **Libraries:** HX711, ArduinoJson, WebSockets  
- **Dokumentation:** `docs/hx711_verkabelung.md`
- **Pi5-Integration:** `wireless/wireless_weight_manager.py`
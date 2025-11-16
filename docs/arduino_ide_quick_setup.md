# ⚡ Arduino IDE Quick-Setup für ESP8266

## ✅ **Status: Arduino IDE installiert!**

```bash
✅ Arduino IDE 1.8.19 installiert
✅ User zu dialout-Gruppe hinzugefügt  
✅ USB-Permissions gesetzt
✅ ESP8266-Sketch geöffnet: wireless/esp8266/futterkarre_wireless_waage_esp8266.ino
```

## 🔧 **Nächste Schritte in Arduino IDE:**

### **1. ESP8266 Board-Support hinzufügen**

In der Arduino IDE:

1. **Datei → Voreinstellungen**
2. **"Zusätzliche Boardverwalter-URLs"** hinzufügen:
   ```
   http://arduino.esp8266.com/stable/package_esp8266com_index.json
   ```
3. **OK** klicken
4. **Tools → Board → Boardverwalter...**  
5. Suche: **"esp8266"**
6. **"ESP8266 Community"** installieren (Version 3.x)

### **2. Erforderliche Libraries installieren**

**Tools → Bibliotheken verwalten**, dann suchen und installieren:

- ✅ **"HX711"** (von Bogdan Necula) - für Wägezellen
- ✅ **"ArduinoJson"** (Version 6.x) - für JSON-Kommunikation  
- ✅ **"WebSockets"** (von Markus Sattler) - für WiFi-Kommunikation

### **3. WiFi-Einstellungen anpassen**

**Im Sketch (Zeilen 30-32) anpassen:**
```cpp
const char* WIFI_SSID = "DEIN_WIFI_NAME";        // ← HIER ÄNDERN
const char* WIFI_PASSWORD = "DEIN_WIFI_PASSWORT"; // ← HIER ÄNDERN
```

### **4. Board konfigurieren**

**ESP8266 NodeMCU anschließen**, dann:

- **Tools → Board: "NodeMCU 1.0 (ESP-12E Module)"**
- **Tools → Port:** (verfügbare Ports werden angezeigt)
- **Tools → Upload Speed: "115200"**
- **Tools → CPU Frequency: "80 MHz"**
- **Tools → Flash Size: "4MB (FS:2MB OTA:~1019KB)"**

### **5. Sketch kompilieren & hochladen**

1. **Sketch → Überprüfen/Kompilieren** ✅ (sollte ohne Fehler)
2. **Sketch → Hochladen** 🚀 (ESP8266 angeschlossen)

**Erwartete Ausgabe:**
```
Kompilierung für Board NodeMCU 1.0 (ESP-12E Module) abgeschlossen.
Der Sketch verwendet 315392 Bytes (30%) des Programmspeicherplatzes.
Hochladen beendet.
```

### **6. Funktionstest**

1. **Tools → Serieller Monitor** (115200 Baud)
2. **ESP8266 Reset-Knopf** drücken

**Sollte anzeigen:**
```
=================================
🚀 Futterkarre Wireless Waage
   ESP8266 NodeMCU Version  
=================================
🔧 GPIO initialisieren... OK
⚖️  HX711 Waagen initialisieren... OK
📡 WiFi verbinden... OK
   IP: 192.168.1.XXX
🔌 WebSocket-Server starten... OK
✅ System bereit!
```

## 🚨 **Häufige Probleme:**

### **Kompilierungs-Fehler:**
```bash
❌ 'WebSocketsServer' was not declared
→ Library "WebSockets" installieren

❌ 'HX711' was not declared  
→ Library "HX711" installieren

❌ Board esp8266:esp8266:nodemcuv2 not found
→ ESP8266 Board-Support installieren (Schritt 1)
```

### **Upload-Fehler:**
```bash
❌ Failed to connect to ESP8266
→ Richtigen Port wählen
→ ESP8266 Reset während Upload drücken

❌ Permission denied /dev/ttyUSB0
→ Terminal schließen und neu öffnen (dialout-Gruppe)
→ Computer neu starten falls nötig
```

### **Runtime-Probleme:**
```bash
❌ WiFi-Verbindung fehlgeschlagen
→ SSID/Passwort im Sketch prüfen (Zeilen 30-32)
→ 2.4GHz WiFi verwenden (nicht 5GHz!)

❌ HX711 nicht bereit
→ HX711 Hardware anschließen
→ Stromversorgung prüfen (5V für HX711)
```

## 📋 **Hardware Pin-Mapping (NodeMCU v3):**

```
ESP8266 NodeMCU Pin-Zuordnung:

HX711_1 (vorne-links):  CLK=D1(GPIO5),  DT=D2(GPIO4)
HX711_2 (vorne-rechts): CLK=D3(GPIO0),  DT=D4(GPIO2)  
HX711_3 (hinten-links): CLK=D5(GPIO14), DT=D6(GPIO12)
HX711_4 (hinten-rechts):CLK=D7(GPIO13), DT=D8(GPIO15)

Power LED (grün):  D0 (GPIO16)
WiFi LED (blau):   Built-in (GPIO2)
Akku-Monitor:      A0 (3.3V max!)
```

## 🎯 **Nach erfolgreichem Flash:**

1. **IP-Adresse notieren** (aus Serial Monitor)
2. **Sketch-Datei speichern** (für zukünftige Updates)
3. **Pi5-Integration:** IP in `wireless/wireless_weight_manager.py` eintragen

---

## 🆘 **Bei Problemen:**

- **Detaillierte Anleitung:** `docs/esp8266_flash_anleitung.md`
- **Hardware-Dokumentation:** `docs/hx711_verkabelung.md`
- **ESP8266 ohne Hardware testen:** Sketch kompiliert auch ohne HX711

**Viel Erfolg beim Flashen! 🚀**
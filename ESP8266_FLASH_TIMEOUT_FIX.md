🚨 ESP8266 FLASH TIMEOUT - SOFORT-LÖSUNG

📊 PROBLEM ANALYSE:
   ✅ Sketch kompiliert erfolgreich (300KB Flash verwendet)
   ✅ ESP8266 NodeMCU erkannt (MAC: d8:bf:c0:01:25:ed)
   ✅ USB-Verbindung funktional (/dev/ttyUSB0)
   ❌ Flash Upload Timeout nach "Running stub..."

🔧 SOFORT-LÖSUNGEN (IN REIHENFOLGE VERSUCHEN):

=== LÖSUNG 1: ESP8266 RESET TIMING ===
1. Arduino IDE geöffnet lassen
2. **WÄHREND** Upload/Connecting Phase:
   - ESP8266 **FLASH-Button** gedrückt halten
   - ESP8266 **RESET-Button** kurz drücken (Flash-Button weiter gedrückt)
   - Flash-Button noch 2-3 Sekunden gedrückt halten
   - Dann loslassen
3. Upload sollte weiterlaufen

=== LÖSUNG 2: UPLOAD SPEED REDUZIEREN ===
Arduino IDE → Tools:
   - Upload Speed: 115200 → **57600** (langsamer aber stabiler)
   - CPU Frequency: 80 MHz (beibehalten)
   - Flash Size: 4MB (beibehalten)

=== LÖSUNG 3: USB-KABEL & POWER ===
   - USB-Kabel fest eingesteckt?
   - Anderen USB-Port versuchen
   - Externes 5V Netzteil für ESP8266 (falls verfügbar)

=== LÖSUNG 4: ESPTOOL MANUAL FLASH ===
Falls Arduino IDE weiter Probleme macht:
```bash
# Kompilierte .bin Datei finden und manuell flashen
find ~/.arduino15/tmp/ -name "*.ino.bin" -mmin -10
```

🎯 **WICHTIG - TIMING IST ALLES:**
Das ESP8266 NodeMCU hat einen "Auto-Flash-Modus", aber manchmal 
muss man den Flash/Reset Timing manuell durchführen.

⚡ **ERFOLGS-ANZEICHEN:**
Nach erfolgreichem Flash sollte Arduino IDE zeigen:
"Hash of data verified. Leaving... Hard resetting via RTS pin..."

📱 **NACH ERFOLGREICHEM FLASH:**
1. Arduino IDE → Tools → Serial Monitor (115200 Baud)
2. ESP8266 Reset-Button drücken  
3. Erwarten: "📊 Dual-Mode WiFi erfolgreich!"

🚀 **VERSUCHEN SIE JETZT LÖSUNG 1 - RESET TIMING!**
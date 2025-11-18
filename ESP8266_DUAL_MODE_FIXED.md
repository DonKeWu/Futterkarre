🚀 ESP8266 DUAL-MODE FIX - BEREIT ZUM FLASHEN!

📊 PROBLEM GELÖST:
   ❌ Vorher: ESP8266 wechselt zu Single-Mode → Verbindung verloren
   ✅ Jetzt: ESP8266 bleibt in Dual-Mode → IP-Präferenz wechselt

🔧 ÄNDERUNGEN GEMACHT:

=== ESP8266 FIRMWARE ===
   ✅ WiFi-Modus-Wechsel ENTFERNT (kein WiFi.mode() mehr)
   ✅ Dual-Mode bleibt IMMER aktiv (AP + Station)
   ✅ Button-Klick ändert nur current_wifi_mode Variable
   ✅ Keine Verbindungsunterbrechung mehr

=== PYTHON GUI ===
   ✅ Kein "ESP startet neu" mehr
   ✅ Direkte IP-Tests nach Modus-Wechsel
   ✅ test_ap_connection() für Stall-Modus
   ✅ test_station_connection() für Haus-Modus

🚀 NÄCHSTER SCHRITT: ESP8266 FLASHEN

**Arduino IDE:**
1. Sketch ist bereits geöffnet
2. Kompilieren (sollte ohne Fehler laufen)
3. Upload mit Manual Boot Mode:
   - USB abziehen
   - FLASH-Button gedrückt halten
   - USB einstecken (Flash weiter gedrückt)
   - Upload starten
   - Flash-Button nach 2-3 Sekunden loslassen

📱 **Nach erfolgreichem Flash:**
   - Serial Monitor: "📊 Dual-Mode WiFi erfolgreich!"
   - GUI-Test: Button-Klicks ohne Verbindungsverlust
   - Beide IPs gleichzeitig erreichbar

🎯 **Das wird funktionieren:**
   🚜 STALL-MODUS → ESP8266 bleibt dual, GUI bevorzugt 192.168.4.1
   🏠 HAUS-MODUS → ESP8266 bleibt dual, GUI bevorzugt 192.168.2.17

✅ **ESP8266 FIX READY - JETZT FLASHEN!**
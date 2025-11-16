#!/usr/bin/env python3
"""
ESP8266 Verbindungstest
Testet WebSocket-Verbindung zum ESP8266 NodeMCU
"""

import asyncio
import websockets
import json
import logging
import subprocess
import socket
from datetime import datetime

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ESP8266Tester:
    def __init__(self):
        self.found_ips = []
        
    def scan_network(self):
        """Scannt das lokale Netzwerk nach ESP8266"""
        logger.info("🔍 Scanne Netzwerk nach ESP8266...")
        
        # Netzwerk-Range bestimmen
        try:
            # IP der Pi5 ermitteln  
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            logger.info(f"Pi5 IP: {local_ip}")
            
            # Netzwerk-Basis (z.B. 192.168.2.x)
            network_base = ".".join(local_ip.split(".")[:-1])
            logger.info(f"Scanne Netzwerk: {network_base}.1-254")
            
            # Ping-Scan für aktive IPs
            active_ips = []
            for i in range(1, 255):
                ip = f"{network_base}.{i}"
                if ip == local_ip:
                    continue
                    
                # Ping testen
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], 
                                     capture_output=True, text=True)
                if result.returncode == 0:
                    active_ips.append(ip)
                    logger.info(f"✅ Aktive IP gefunden: {ip}")
            
            return active_ips
            
        except Exception as e:
            logger.error(f"Netzwerk-Scan Fehler: {e}")
            return []
    
    async def test_websocket(self, ip: str, port: int = 81) -> bool:
        """Testet WebSocket-Verbindung zu einer IP"""
        try:
            uri = f"ws://{ip}:{port}"
            logger.info(f"🔌 Teste WebSocket: {uri}")
            
            # Verbindung mit Timeout
            websocket = await asyncio.wait_for(
                websockets.connect(uri), timeout=5.0
            )
            
            logger.info(f"✅ WebSocket-Verbindung erfolgreich: {ip}:{port}")
            
            # Status-Kommando senden
            status_cmd = {"command": "get_status"}
            await websocket.send(json.dumps(status_cmd))
            
            # Antwort empfangen
            response = await asyncio.wait_for(websocket.recv(), timeout=5.0)
            data = json.loads(response)
            
            logger.info(f"📊 ESP8266-Response: {data}")
            
            # Verbindung schließen
            await websocket.close()
            return True
            
        except asyncio.TimeoutError:
            logger.warning(f"⏱️  Timeout bei {ip}:{port}")
            return False
        except ConnectionRefusedError:
            logger.debug(f"❌ Connection refused: {ip}:{port}")
            return False
        except Exception as e:
            logger.debug(f"❌ WebSocket-Test fehlgeschlagen ({ip}): {e}")
            return False
    
    async def find_esp8266(self):
        """Sucht ESP8266 im Netzwerk"""
        logger.info("🚀 ESP8266 Suche gestartet...")
        
        # Netzwerk scannen
        active_ips = self.scan_network()
        
        if not active_ips:
            logger.warning("❌ Keine aktiven IPs im Netzwerk gefunden!")
            return []
        
        # WebSocket-Tests parallel
        logger.info(f"🔌 Teste {len(active_ips)} IPs auf WebSocket (Port 81)...")
        tasks = [self.test_websocket(ip) for ip in active_ips]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # ESP8266 IPs sammeln
        esp8266_ips = []
        for ip, result in zip(active_ips, results):
            if result is True:
                esp8266_ips.append(ip)
        
        return esp8266_ips
    
    async def test_weight_data(self, ip: str):
        """Testet Gewichtsdaten-Stream vom ESP8266"""
        try:
            uri = f"ws://{ip}:81"
            logger.info(f"📊 Teste Gewichtsdaten von {ip}...")
            
            websocket = await websockets.connect(uri)
            
            # 10 Sekunden Gewichtsdaten sammeln
            logger.info("⏱️  Sammle 10 Sekunden Gewichtsdaten...")
            weight_count = 0
            start_time = asyncio.get_event_loop().time()
            
            while asyncio.get_event_loop().time() - start_time < 10:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=2.0)
                    data = json.loads(message)
                    
                    if data.get("type") == "weight_data":
                        weight_count += 1
                        total_kg = data.get("total_kg", 0)
                        corners = data.get("corners", [])
                        battery = data.get("battery_v", 0)
                        rssi = data.get("wifi_rssi", 0)
                        
                        logger.info(f"⚖️  #{weight_count}: {total_kg:.2f}kg, "
                                  f"Ecken: {corners}, Akku: {battery:.1f}V, RSSI: {rssi}dBm")
                
                except asyncio.TimeoutError:
                    logger.debug("Keine Gewichtsdaten empfangen")
                    continue
            
            await websocket.close()
            logger.info(f"✅ Gewichtsdaten-Test abgeschlossen: {weight_count} Datenpakete empfangen")
            return weight_count > 0
            
        except Exception as e:
            logger.error(f"❌ Gewichtsdaten-Test fehlgeschlagen: {e}")
            return False

async def main():
    """Haupt-Test-Routine"""
    print("=" * 60)
    print("🔍 ESP8266 Verbindungstest")
    print("=" * 60)
    
    tester = ESP8266Tester()
    
    # 1. ESP8266 suchen
    esp8266_ips = await tester.find_esp8266()
    
    if not esp8266_ips:
        print("\n❌ Kein ESP8266 gefunden!")
        print("\n🔧 Troubleshooting:")
        print("   1. ESP8266 eingeschaltet und WiFi verbunden?")
        print("   2. Gleisches WiFi-Netzwerk wie Pi5?")
        print("   3. Serial Monitor: ESP8266 IP-Adresse notieren")
        print("   4. Firewall/Router-Einstellungen prüfen")
        return False
    
    print(f"\n✅ ESP8266 gefunden: {esp8266_ips}")
    
    # 2. Gewichtsdaten testen
    for ip in esp8266_ips:
        success = await tester.test_weight_data(ip)
        if success:
            print(f"\n🎉 ESP8266 voll funktionsfähig: {ip}")
            print(f"   WebSocket-URL für Pi5: ws://{ip}:81")
            
            # Integration-Hinweis
            print(f"\n📝 Für Pi5-Integration:")
            print(f"   1. IP in wireless/wireless_weight_manager.py eintragen: '{ip}'")
            print(f"   2. Test mit: python test_wireless_integration.py {ip}")
            
            return True
    
    print(f"\n⚠️  ESP8266 reagiert, aber keine Gewichtsdaten")
    return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test abgebrochen")
        exit(1)
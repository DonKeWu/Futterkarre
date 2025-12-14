#!/usr/bin/env python3
"""
Pi5 System Test für ESP8266+HX711 Setup
Alle Tests die auf dem Pi5 ausgeführt werden können
"""

import sys
import time
import json
import subprocess
import urllib.request
from datetime import datetime

def test_pi5_system():
    """Basis Pi5 System Test"""
    print("🔧 PI5 SYSTEM TEST")
    print("=" * 30)
    
    try:
        # Python Version
        python_version = sys.version.split()[0]
        print(f"✅ Python: {python_version}")
        
        # Wichtige Module
        modules = ['json', 'urllib', 'subprocess', 'datetime', 'time']
        for module in modules:
            try:
                __import__(module)
                print(f"✅ {module}: OK")
            except ImportError:
                print(f"❌ {module}: FEHLT")
        
        # Memory Check
        try:
            with open('/proc/meminfo', 'r') as f:
                for line in f:
                    if 'MemAvailable' in line:
                        mem_mb = int(line.split()[1]) // 1024
                        print(f"💾 RAM verfügbar: {mem_mb}MB")
                        break
        except:
            print("❌ RAM Info nicht verfügbar")
        
        return True
        
    except Exception as e:
        print(f"❌ Pi5 System Test fehlgeschlagen: {e}")
        return False

def test_network_connectivity():
    """Test Netzwerk-Verbindung"""
    print("\n🌐 NETZWERK-TEST")
    print("=" * 30)
    
    try:
        # Internet-Test
        result = subprocess.run(['ping', '-c', '2', '8.8.8.8'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Internet-Verbindung: OK")
        else:
            print("❌ Internet-Verbindung: FEHLER")
        
        # Lokales Netzwerk
        try:
            result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
            if result.returncode == 0:
                ip = result.stdout.strip()
                print(f"🏠 Pi5 IP-Adresse: {ip}")
            else:
                print("❌ IP-Adresse nicht ermittelbar")
        except:
            print("❌ IP-Test fehlgeschlagen")
        
        return True
        
    except Exception as e:
        print(f"❌ Netzwerk-Test fehlgeschlagen: {e}")
        return False

def test_esp8266_discovery():
    """Suche nach ESP8266 im Netzwerk"""
    print("\n📡 ESP8266 DISCOVERY")
    print("=" * 35)
    
    # IP-Ranges für lokales Netzwerk
    ip_ranges = [
        "192.168.1.{}",   # Häufigste Router-Range
        "192.168.2.{}",   # Alternative Range  
        "192.168.0.{}",   # Weitere Alternative
        "10.0.0.{}"       # Manche Router
    ]
    
    found_devices = []
    
    # Teste bekannte IPs zuerst
    known_ips = ["192.168.2.20", "192.168.4.1"]
    
    print("🔍 Teste bekannte ESP8266-IPs...")
    for ip in known_ips:
        if test_single_esp8266(ip):
            found_devices.append(ip)
    
    if found_devices:
        print(f"✅ ESP8266 gefunden: {found_devices}")
        return found_devices
    
    # Erweiterte Suche im lokalen Netz
    print("🔍 Erweiterte Netzwerk-Suche...")
    
    # Nur einige IPs testen (nicht das ganze Netz - das dauert zu lange)
    test_ips = []
    for ip_template in ip_ranges[:2]:  # Nur erste 2 Ranges
        for last_octet in [1, 10, 20, 50, 100, 150, 200]:
            test_ips.append(ip_template.format(last_octet))
    
    for ip in test_ips:
        if test_single_esp8266(ip, timeout=1):
            found_devices.append(ip)
            if len(found_devices) >= 3:  # Max 3 Devices suchen
                break
    
    if found_devices:
        print(f"✅ ESP8266-Devices gefunden: {found_devices}")
    else:
        print("❌ Keine ESP8266-Devices gefunden")
    
    return found_devices

def test_single_esp8266(ip, timeout=3):
    """Teste einzelne ESP8266-IP"""
    try:
        url = f"http://{ip}/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Pi5-Futterkarre'})
        
        with urllib.request.urlopen(req, timeout=timeout) as response:
            if response.status == 200:
                print(f"✅ ESP8266 antwortet: {ip}")
                return True
            else:
                return False
                
    except:
        return False

def test_esp8266_hx711_functionality(esp_ips):
    """Teste HX711-Funktionalität über ESP8266"""
    print("\n⚖️ ESP8266+HX711 FUNKTIONS-TEST")
    print("=" * 45)
    
    working_devices = []
    
    for ip in esp_ips:
        print(f"\n🔍 Teste {ip}...")
        
        try:
            # Status abrufen
            status_url = f"http://{ip}/status"
            req = urllib.request.Request(status_url)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                status_data = json.loads(response.read().decode('utf-8'))
                print(f"✅ Status erhalten: {status_data}")
                
            # Gewicht abrufen
            weight_url = f"http://{ip}/weight"
            req = urllib.request.Request(weight_url)
            
            with urllib.request.urlopen(req, timeout=5) as response:
                weight_data = json.loads(response.read().decode('utf-8'))
                
                weight = weight_data.get('total_weight', 0.0)
                cells = weight_data.get('cells', [])
                
                print(f"⚖️ Gewicht: {weight:.3f}kg")
                print(f"🔍 Zellen: {cells}")
                
                working_devices.append({
                    'ip': ip,
                    'weight': weight,
                    'cells': cells,
                    'status': status_data
                })
                
        except Exception as e:
            print(f"❌ {ip}: {e}")
    
    return working_devices

def run_comprehensive_test():
    """Führt alle Tests aus"""
    print("🚀 UMFASSENDER PI5 + ESP8266 + HX711 TEST")
    print("=" * 60)
    print(f"⏰ Start: {datetime.now().strftime('%H:%M:%S')}")
    print("🔌 Setup: Pi5 ←WiFi→ ESP8266 ←GPIO→ HX711")
    print("=" * 60)
    
    results = {}
    
    # 1. Pi5 System Test
    results['pi5_system'] = test_pi5_system()
    
    # 2. Netzwerk Test
    results['network'] = test_network_connectivity()
    
    # 3. ESP8266 Discovery
    if results['network']:
        esp_ips = test_esp8266_discovery()
        results['esp8266_found'] = len(esp_ips) > 0
        results['esp8266_ips'] = esp_ips
    else:
        esp_ips = []
        results['esp8266_found'] = False
        results['esp8266_ips'] = []
    
    # 4. HX711 Funktions-Test
    if esp_ips:
        working_devices = test_esp8266_hx711_functionality(esp_ips)
        results['hx711_working'] = len(working_devices) > 0
        results['working_devices'] = working_devices
    else:
        results['hx711_working'] = False
        results['working_devices'] = []
    
    # Ergebnis-Zusammenfassung
    print(f"\n📊 TEST-ZUSAMMENFASSUNG")
    print("=" * 40)
    print(f"🔧 Pi5 System: {'✅ OK' if results['pi5_system'] else '❌ FEHLER'}")
    print(f"🌐 Netzwerk: {'✅ OK' if results['network'] else '❌ FEHLER'}")
    print(f"📡 ESP8266: {'✅ Gefunden' if results['esp8266_found'] else '❌ Nicht gefunden'}")
    print(f"⚖️ HX711: {'✅ Funktional' if results['hx711_working'] else '❌ Nicht funktional'}")
    
    if results['working_devices']:
        print(f"\n✅ FUNKTIONALE GERÄTE:")
        for device in results['working_devices']:
            print(f"   📍 {device['ip']}: {device['weight']:.3f}kg")
    
    # Empfehlungen
    print(f"\n💡 EMPFEHLUNGEN:")
    if not results['network']:
        print("   - Netzwerk-Verbindung prüfen")
    elif not results['esp8266_found']:
        print("   - ESP8266 einschalten und WiFi-Verbindung prüfen")
        print("   - IP-Adresse des ESP8266 überprüfen")
    elif not results['hx711_working']:
        print("   - ESP8266-Firmware und HX711-Verkabelung prüfen")
        print("   - Wägezellen-Anschluss kontrollieren")
    else:
        print("   🎉 System vollständig funktional!")
    
    return results

def main():
    """Hauptprogramm"""
    if len(sys.argv) > 1 and sys.argv[1] == "quick":
        # Schneller Test
        test_pi5_system()
        esp_ips = ["192.168.2.20"]  # Bekannte IP
        if test_single_esp8266(esp_ips[0]):
            test_esp8266_hx711_functionality(esp_ips)
    else:
        # Vollständiger Test
        run_comprehensive_test()
    
    print(f"\n🏁 Test abgeschlossen: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()
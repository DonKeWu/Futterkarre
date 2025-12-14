#!/usr/bin/env python3
"""
ESP8266 + HX711 Test - für WiFi-basierte Gewichtssensoren
Pi5 testet ESP8266 über Netzwerk, ESP8266 hat HX711 angeschlossen
"""

import sys
import time
import json
import urllib.request
import urllib.error
from datetime import datetime

def test_esp8266_connection():
    """Teste ESP8266 Netzwerk-Verbindung"""
    print("📡 ESP8266 NETZWERK-TEST")
    print("=" * 40)
    
    # Bekannte ESP8266 IP-Adressen testen
    test_ips = [
        "192.168.2.20",   # Deine aktuelle IP
        "192.168.4.1",   # ESP8266 AP Mode
        "192.168.1.100", # Häufige Router-IP-Range
        "192.168.0.100"  # Alternative Router-Range
    ]
    
    working_ips = []
    
    for ip in test_ips:
        print(f"🔍 Teste ESP8266 auf {ip}...")
        
        try:
            # Einfacher HTTP-Request
            url = f"http://{ip}/"
            req = urllib.request.Request(url, headers={'User-Agent': 'Futterkarre-Pi5'})
            
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status == 200:
                    content = response.read().decode('utf-8')
                    print(f"✅ ESP8266 gefunden auf {ip}")
                    print(f"   Response: {content[:100]}...")
                    working_ips.append(ip)
                else:
                    print(f"⚠️ {ip}: HTTP {response.status}")
                    
        except urllib.error.URLError as e:
            print(f"❌ {ip}: {e}")
        except Exception as e:
            print(f"❌ {ip}: Unbekannter Fehler - {e}")
    
    return working_ips

def test_esp8266_hx711_data(ip):
    """Teste HX711-Daten vom ESP8266"""
    print(f"\n⚖️ HX711-DATEN TEST für {ip}")
    print("=" * 50)
    
    try:
        # Status-Endpoint
        status_url = f"http://{ip}/status"
        print(f"📋 Status-Request: {status_url}")
        
        req = urllib.request.Request(status_url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status_data = json.loads(response.read().decode('utf-8'))
            
            print("✅ Status-Daten erhalten:")
            for key, value in status_data.items():
                print(f"   {key}: {value}")
                
            return status_data
            
    except json.JSONDecodeError as e:
        print(f"❌ JSON-Parse-Fehler: {e}")
    except Exception as e:
        print(f"❌ Status-Request fehlgeschlagen: {e}")
        
    try:
        # Weight-Endpoint 
        weight_url = f"http://{ip}/weight"
        print(f"\n📊 Weight-Request: {weight_url}")
        
        req = urllib.request.Request(weight_url)
        with urllib.request.urlopen(req, timeout=5) as response:
            weight_data = json.loads(response.read().decode('utf-8'))
            
            print("✅ Gewichts-Daten erhalten:")
            for key, value in weight_data.items():
                print(f"   {key}: {value}")
                
            return weight_data
            
    except Exception as e:
        print(f"❌ Weight-Request fehlgeschlagen: {e}")
    
    return None

def test_esp8266_hx711_live_data(ip, count=5):
    """Live-Test der HX711-Daten über ESP8266"""
    print(f"\n🔄 LIVE HX711-DATEN TEST ({count} Messungen)")
    print("=" * 60)
    
    measurements = []
    
    for i in range(count):
        print(f"\n📊 Messung {i+1}/{count}:")
        
        try:
            # Gewicht abrufen
            weight_url = f"http://{ip}/weight"
            req = urllib.request.Request(weight_url)
            
            start_time = time.time()
            with urllib.request.urlopen(req, timeout=5) as response:
                end_time = time.time()
                response_time = (end_time - start_time) * 1000  # ms
                
                data = json.loads(response.read().decode('utf-8'))
                
                # Daten extrahieren
                weight = data.get('total_weight', 0.0)
                cells = data.get('cells', [0, 0, 0, 0])
                
                print(f"   ⚖️  Gesamtgewicht: {weight:.3f}kg")
                print(f"   🔍 Einzelzellen: {cells}")
                print(f"   ⏱️  Response-Zeit: {response_time:.1f}ms")
                
                measurements.append({
                    'weight': weight,
                    'cells': cells,
                    'response_time': response_time,
                    'timestamp': datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"   ❌ Fehler: {e}")
            
        if i < count - 1:
            time.sleep(0.5)
    
    # Statistik
    if measurements:
        print(f"\n📈 STATISTIK ({len(measurements)} erfolgreiche Messungen)")
        print("=" * 50)
        
        weights = [m['weight'] for m in measurements]
        response_times = [m['response_time'] for m in measurements]
        
        print(f"⚖️  Gewicht:")
        print(f"   Durchschnitt: {sum(weights)/len(weights):.3f}kg")
        print(f"   Min: {min(weights):.3f}kg")
        print(f"   Max: {max(weights):.3f}kg")
        print(f"   Schwankung: ±{(max(weights)-min(weights))/2:.3f}kg")
        
        print(f"⏱️  Response-Zeit:")
        print(f"   Durchschnitt: {sum(response_times)/len(response_times):.1f}ms")
        print(f"   Min: {min(response_times):.1f}ms")
        print(f"   Max: {max(response_times):.1f}ms")
    
    return measurements

def main():
    print("🚀 ESP8266 + HX711 SYSTEM TEST")
    print("=" * 50)
    print("🔌 Architektur: Pi5 ←WiFi→ ESP8266 ←GPIO→ HX711 ←→ Wägezellen")
    print("=" * 50)
    
    # 1. ESP8266 Netzwerk-Test
    working_ips = test_esp8266_connection()
    
    if not working_ips:
        print("\n❌ KEIN ESP8266 GEFUNDEN!")
        print("🔧 Prüfungen:")
        print("   - ESP8266 eingeschaltet?")
        print("   - Im selben WiFi-Netzwerk?") 
        print("   - Firmware läuft korrekt?")
        print("   - IP-Adresse korrekt?")
        return False
    
    print(f"\n✅ {len(working_ips)} ESP8266 gefunden: {working_ips}")
    
    # 2. Teste jeden gefundenen ESP8266
    for ip in working_ips:
        print(f"\n{'='*60}")
        print(f"🎯 TESTE ESP8266: {ip}")
        print(f"{'='*60}")
        
        # Status & HX711-Daten
        status = test_esp8266_hx711_data(ip)
        
        # Live-Tests
        measurements = test_esp8266_hx711_live_data(ip, count=5)
        
        # Bewertung
        if measurements and len(measurements) >= 3:
            weights = [m['weight'] for m in measurements]
            if any(w > 0.001 for w in weights):  # Mindestens 1g
                print(f"✅ ESP8266 {ip}: HX711-System funktional!")
            else:
                print(f"⚠️ ESP8266 {ip}: Nur Nullwerte - HX711/Wägezelle prüfen")
        else:
            print(f"❌ ESP8266 {ip}: Keine stabilen Messungen")
    
    print(f"\n🎉 TEST ABGESCHLOSSEN")
    print("💡 Bei Problemen: ESP8266-Firmware und HX711-Verkabelung prüfen")
    
    return True

if __name__ == "__main__":
    main()
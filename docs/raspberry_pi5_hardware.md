# 🍓 Raspberry Pi 5 - Hardware-Integration Plan

## 📋 **Raspberry Pi 5 Spezifikationen**

### **Hardware-Übersicht:**
- **CPU:** Broadcom BCM2712 (Quad-core ARM Cortex-A76, 2.4GHz)
- **RAM:** 4GB/8GB LPDDR4X-4267 SDRAM
- **GPIO:** 40-pin Standard-Header (kompatibel mit RPi 4)
- **USB:** 2x USB 3.0, 2x USB 2.0
- **Ethernet:** Gigabit
- **Display:** 2x 4Kp60 HDMI
- **Stromverbrauch:** ~5W (deutlich effizienter als RPi 4)

### **Vorteile für Futterkarre 2.0:**
- **2-3x schneller** als RPi 4 → flüssige PyQt5-UI
- **Verbesserte GPU** → bessere Touch-Response
- **Niedrigerer Stromverbrauch** → längere Akkulaufzeit
- **PCIe-Support** → Erweiterungsmöglichkeiten
- **Verbesserte I/O** → stabilere Sensor-Anbindung

---

## 🔌 **Hardware-Anbindung**

### **HX711 Wägesensoren (4x für Karren-Ecken):**
```
RPi5 GPIO → HX711 Module
├── GPIO 5  (Pin 29) → HX711_1 DT  (Data)
├── GPIO 6  (Pin 31) → HX711_1 SCK (Clock)
├── GPIO 13 (Pin 33) → HX711_2 DT
├── GPIO 19 (Pin 35) → HX711_2 SCK
├── GPIO 26 (Pin 37) → HX711_3 DT
├── GPIO 21 (Pin 40) → HX711_3 SCK
├── GPIO 20 (Pin 38) → HX711_4 DT
└── GPIO 16 (Pin 36) → HX711_4 SCK

Stromversorgung:
├── 5V (Pin 2/4) → VCC aller HX711-Module
└── GND (Pin 6/9/14/20/25/30/34/39) → GND
```

### **7" Touchscreen (offiziell oder kompatibel):**
```
RPi5 → Touchscreen
├── DSI-Port → Display-Kabel
├── GPIO → Touch-Controller (I2C)
├── 5V/GND → Stromversorgung
└── USB → Touch-Input (fallback)
```

### **Zusätzliche Hardware:**
```
├── 🔋 Akku: 12V LiFePO4 (20Ah) + Step-Down auf 5V
├── 🛡️ Gehäuse: IP65 Industriegehäuse
├── 💾 SD-Karte: 64GB Class 10 (Raspi OS Lite)
├── 🌡️ Temperatursensor: DS18B20 (optional)
└── 📶 WiFi: Integriert (Daten-Backup)
```

---

## ⚙️ **Software-Konfiguration**

### **Raspberry Pi OS Setup:**
```bash
# 1. Raspberry Pi Imager verwenden
# - OS: Raspberry Pi OS Lite (64-bit)
# - SSH aktivieren
# - WiFi konfigurieren

# 2. Grundsystem aktualisieren
sudo apt update && sudo apt upgrade -y

# 3. Python-Abhängigkeiten
sudo apt install python3-pip python3-venv python3-pyqt5
sudo apt install python3-gpio python3-spidev
pip3 install hx711 RPi.GPIO pandas
```

### **Hardware-Aktivierung:**
```bash
# /boot/config.txt Anpassungen
echo "# Futterkarre 2.0 Hardware Config" >> /boot/config.txt
echo "dtparam=spi=on" >> /boot/config.txt
echo "dtparam=i2c_arm=on" >> /boot/config.txt
echo "dtoverlay=dwc2" >> /boot/config.txt

# GPIO-Berechtigungen
sudo usermod -a -G gpio,spi,i2c pi
```

---

## 🔧 **Code-Anpassungen für RPi5**

### **Hardware-Detection verbessern:**
```python
# hardware/rpi5_detector.py
import os
import subprocess

class RPi5Detector:
    @staticmethod
    def is_raspberry_pi5():
        """Erkennt Raspberry Pi 5 zuverlässig"""
        try:
            # CPU-Info prüfen
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
                if 'BCM2712' in cpuinfo:
                    return True
            
            # Device Tree prüfen
            if os.path.exists('/proc/device-tree/model'):
                with open('/proc/device-tree/model', 'r') as f:
                    model = f.read()
                    if 'Raspberry Pi 5' in model:
                        return True
            
            return False
        except:
            return False
    
    @staticmethod
    def get_gpio_version():
        """GPIO-Library Version für RPi5"""
        try:
            result = subprocess.run(['gpio', 'readall'], 
                                  capture_output=True, text=True)
            return "RPi5-compatible" if result.returncode == 0 else "legacy"
        except:
            return "unknown"
```

### **Erweiterte Sensor-Abstraktion:**
```python
# hardware/rpi5_sensors.py
from hardware.rpi5_detector import RPi5Detector
import RPi.GPIO as GPIO

class RPi5SensorManager:
    def __init__(self):
        self.is_rpi5 = RPi5Detector.is_raspberry_pi5()
        self.hx711_configs = [
            {'dt_pin': 5, 'sck_pin': 6, 'name': 'Ecke_VL'},
            {'dt_pin': 13, 'sck_pin': 19, 'name': 'Ecke_VR'},
            {'dt_pin': 26, 'sck_pin': 21, 'name': 'Ecke_HL'},
            {'dt_pin': 20, 'sck_pin': 16, 'name': 'Ecke_HR'}
        ]
        self.init_gpio()
    
    def init_gpio(self):
        """GPIO für RPi5 optimiert initialisieren"""
        if self.is_rpi5:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            # RPi5-spezifische Optimierungen
            for config in self.hx711_configs:
                GPIO.setup(config['dt_pin'], GPIO.IN)
                GPIO.setup(config['sck_pin'], GPIO.OUT)
```

---

## 🔋 **Stromversorgung & Gehäuse**

### **Akku-Dimensionierung:**
```
Komponente                 | Stromverbrauch
---------------------------|---------------
Raspberry Pi 5             | 5W (1A @ 5V)
Touchscreen 7"             | 4W (0.8A @ 5V)  
4x HX711-Module            | 0.5W (0.1A @ 5V)
Kühlung (Lüfter)          | 1W (0.2A @ 5V)
---------------------------|---------------
Gesamt                     | ~11W (2.2A @ 5V)

Akku-Laufzeit (20Ah LiFePO4):
20Ah ÷ 2.2A = ~9 Stunden Dauerbetrieb
```

### **Gehäuse-Anforderungen:**
- **Schutzart:** IP65 (staub-/wasserdicht)
- **Material:** Aluminium oder robuster Kunststoff
- **Abmessungen:** ~250x200x100mm
- **Kühlung:** Passive Kühlung + kleiner Lüfter
- **Zugänglichkeit:** SD-Karte, USB-Ports

---

## 📱 **Touch-Optimierung**

### **Display-Konfiguration:**
```bash
# /boot/config.txt für optimale Touch-Performance
echo "# Display-Optimierung für Futterkarre" >> /boot/config.txt
echo "lcd_rotate=2" >> /boot/config.txt  # Falls Display gedreht
echo "disable_overscan=1" >> /boot/config.txt
echo "hdmi_force_hotplug=1" >> /boot/config.txt
echo "hdmi_group=2" >> /boot/config.txt
echo "hdmi_mode=87" >> /boot/config.txt
echo "hdmi_cvt=1024 600 60 6 0 0 0" >> /boot/config.txt
```

### **PyQt5-Touch-Anpassungen:**
```python
# views/touch_optimizer.py
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication

class TouchOptimizer:
    @staticmethod
    def optimize_for_rpi5():
        """Touch-Response für RPi5 optimieren"""
        app = QApplication.instance()
        if app:
            # Touch-Delay reduzieren
            app.setDoubleClickInterval(300)
            # Scroll-Verhalten anpassen  
            app.setWheelScrollLines(1)
            # High-DPI für RPi5 aktivieren
            app.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
```

---

## 🧪 **Testing & Kalibrierung**

### **Hardware-Tests:**
```python
# tests/test_rpi5_hardware.py
def test_hx711_sensors():
    """Teste alle 4 HX711-Sensoren"""
    sensor_manager = RPi5SensorManager()
    for i, config in enumerate(sensor_manager.hx711_configs):
        weight = sensor_manager.read_sensor(i)
        assert weight is not None, f"Sensor {config['name']} nicht erreichbar"
        assert 0 <= weight <= 1000, f"Sensor {config['name']}: unrealistisches Gewicht"

def test_gpio_performance():
    """GPIO-Performance auf RPi5 testen"""
    import time
    start = time.time()
    for _ in range(1000):
        GPIO.output(6, GPIO.HIGH)
        GPIO.output(6, GPIO.LOW)
    duration = time.time() - start
    assert duration < 0.1, "GPIO zu langsam für Echtzeitanwendung"
```

### **Kalibrierung-Wizard:**
```python
# utils/rpi5_calibration.py
class CalibrationWizard:
    def __init__(self):
        self.known_weights = [0, 5, 10, 20, 50]  # kg
        self.calibration_data = {}
    
    def calibrate_sensor(self, sensor_id):
        """Interaktive Sensor-Kalibrierung"""
        print(f"Kalibrierung Sensor {sensor_id}")
        for weight in self.known_weights:
            input(f"Lege {weight}kg auf und drücke Enter...")
            raw_value = self.read_raw_sensor(sensor_id)
            self.calibration_data[weight] = raw_value
        
        # Lineare Regression für Kalibrierungsfunktion
        self.calculate_calibration_function(sensor_id)
```

---

## 📦 **Deployment & Installation**

### **Automatische Installation:**
```bash
#!/bin/bash
# install_rpi5.sh - Automatisches Setup

echo "🍓 Futterkarre 2.0 - RPi5 Installation"

# 1. System Update
sudo apt update && sudo apt upgrade -y

# 2. Dependencies
sudo apt install -y python3-pip python3-venv python3-pyqt5
sudo apt install -y python3-gpio python3-spidev git

# 3. Repository klonen
git clone https://github.com/DonKeWu/Futterkarre-2.git
cd Futterkarre-2

# 4. Virtual Environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_rpi5.txt

# 5. Hardware konfigurieren
sudo python3 setup_rpi5_hardware.py

# 6. Service installieren
sudo cp systemd/futterkarre.service /etc/systemd/system/
sudo systemctl enable futterkarre.service

echo "✅ Installation abgeschlossen!"
echo "Starte mit: sudo systemctl start futterkarre"
```

### **Systemd Service:**
```ini
# systemd/futterkarre.service
[Unit]
Description=Futterkarre 2.0 - Intelligente Futterwaage
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Futterkarre-2
Environment=DISPLAY=:0
ExecStart=/home/pi/Futterkarre-2/venv/bin/python main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 🔄 **Update & Wartung**

### **Remote Update System:**
```python
# utils/remote_updater.py
class RemoteUpdater:
    def __init__(self):
        self.repo_url = "https://github.com/DonKeWu/Futterkarre-2.git"
        self.backup_dir = "/home/pi/futterkarre_backup"
    
    def check_for_updates(self):
        """Prüfe auf GitHub-Updates"""
        result = subprocess.run(
            ['git', 'fetch', '--dry-run'], 
            capture_output=True, text=True
        )
        return len(result.stderr) > 0
    
    def create_backup(self):
        """Backup vor Update"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.backup_dir}/backup_{timestamp}"
        shutil.copytree(".", backup_path, ignore=shutil.ignore_patterns('.git'))
    
    def apply_update(self):
        """Sicheres Update durchführen"""
        self.create_backup()
        subprocess.run(['git', 'pull', 'origin', 'main'])
        subprocess.run(['sudo', 'systemctl', 'restart', 'futterkarre'])
```

---

**🎯 Nächste Schritte:** 
1. Hardware bestellen (RPi5, Sensoren, Gehäuse)
2. Breadboard-Prototyp aufbauen
3. Software-Tests durchführen
4. Gehäuse-Integration & Kalibrierung
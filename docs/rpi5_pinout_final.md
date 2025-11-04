# 📍 Raspberry Pi 5 GPIO Pin-Belegung für Futterkarre 2.0

## 🔌 **HX711 Wägezellen-Anschlüsse**

```
Raspberry Pi 5 GPIO-Header (40-pin):

        3V3  (1) (2)  5V    ← HX711_1 + HX711_3 VCC
       GPIO2 (3) (4)  5V    ← HX711_2 + HX711_4 VCC
       GPIO3 (5) (6)  GND   ← HX711_1 GND
       GPIO4 (7) (8)  GPIO14
         GND (9) (10) GPIO15 ← HX711_2 GND
      GPIO17 (11)(12) GPIO18
      GPIO27 (13)(14) GND   ← HX711_3 GND
      GPIO22 (15)(16) GPIO23
        3V3 (17)(18) GPIO24
      GPIO10 (19)(20) GND   ← HX711_4 GND
       GPIO9 (21)(22) GPIO25
      GPIO11 (23)(24) GPIO8
         GND (25)(26) GPIO7
       GPIO0 (27)(28) GPIO1
   ↗  GPIO5 (29)(30) GND
   ↗  GPIO6 (31)(32) GPIO12
   ↗ GPIO13 (33)(34) GND
   ↗ GPIO19 (35)(36) GPIO16 ↙
   ↗ GPIO26 (37)(38) GPIO20 ↙
         GND (39)(40) GPIO21 ↙
```

## 📋 **HX711 Pin-Zuordnung**

| Wägezelle | Position | DT (Data) | SCK (Clock) | VCC | GND |
|-----------|----------|-----------|-------------|-----|-----|
| **WZ1** | Vorne Links | GPIO 5 (Pin 29) | GPIO 6 (Pin 31) | Pin 2 (5V) | Pin 6 (GND) |
| **WZ2** | Vorne Rechts | GPIO 13 (Pin 33) | GPIO 19 (Pin 35) | Pin 4 (5V) | Pin 9 (GND) |
| **WZ3** | Hinten Links | GPIO 26 (Pin 37) | GPIO 21 (Pin 40) | Pin 2 (5V) | Pin 14 (GND) |
| **WZ4** | Hinten Rechts | GPIO 20 (Pin 38) | GPIO 16 (Pin 36) | Pin 4 (5V) | Pin 20 (GND) |

## 🔧 **Code-Konfiguration**

```python
# hardware/hx711_real.py - Pin-Definitionen:
hx711_configs = [
    {'dt_pin': 5, 'sck_pin': 6, 'name': 'Vorne_Links'},     # WZ1
    {'dt_pin': 13, 'sck_pin': 19, 'name': 'Vorne_Rechts'},  # WZ2  
    {'dt_pin': 26, 'sck_pin': 21, 'name': 'Hinten_Links'},  # WZ3
    {'dt_pin': 20, 'sck_pin': 16, 'name': 'Hinten_Rechts'}  # WZ4
]
```

## ⚡ **Stromversorgung**

```
5V-Verteilung:
├── Pin 2 (5V): HX711_1 + HX711_3 parallel
└── Pin 4 (5V): HX711_2 + HX711_4 parallel

GND-Verteilung:
├── Pin 6: HX711_1    ├── Pin 14: HX711_3
└── Pin 9: HX711_2    └── Pin 20: HX711_4

Stromverbrauch: 4x 10mA = 40mA (Pi 5 kann bis 1.6A)
```

## 🆓 **Freie GPIO-Pins für Erweiterungen**

```
Verfügbare Pins für zusätzliche Hardware:
├── GPIO 2, 3 (I2C) - für Sensoren (Temperatur, etc.)
├── GPIO 4, 17, 27, 22 - für Relais, LEDs
├── GPIO 18 (PWM) - für Servo/Motor-Steuerung
├── GPIO 14, 15 (UART) - für serielle Kommunikation
└── GPIO 10, 11, 8, 9 (SPI) - für Display/Speicher
```
# hardware/hx711_sim.py - KORRIGIERTE VERSION
import random
import sys

# Nur EINE Variable!
USE_SIMULATION = False

def setze_simulation(enabled: bool):
    """Schaltet Simulation ein/aus"""
    global USE_SIMULATION
    USE_SIMULATION = enabled
    print(f"HX711 Simulation: {'Ein' if enabled else 'Aus'}")

def ist_simulation_aktiv():
    """Prüft ob HX711-Simulation aktiv ist"""
    return USE_SIMULATION

def simuliere_gewicht():
    """Simuliert realistisches Karrengewicht (15-45kg)"""
    return round(random.uniform(15.0, 45.0), 2)

def lese_einzelzellen():
    """Simuliert 4 einzelne Wägezellen für Debugging"""
    if USE_SIMULATION:
        return [round(random.uniform(3.0, 12.0), 2) for _ in range(4)]
    else:
        return [0.0, 0.0, 0.0, 0.0]

# Kompatibilitätsfunktion
def lese_gewicht():
    """Kompatibilitätsfunktion für alten Code"""
    if USE_SIMULATION:
        return simuliere_gewicht()
    return 0.0



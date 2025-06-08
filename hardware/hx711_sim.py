# hardware/hx711_sim.py

import sys
import random

USE_SIMULATION = True

def setze_simulation(an):
    global USE_SIMULATION
    USE_SIMULATION = an

def simuliere_gewicht():
    return round(random.uniform(0, 100), 2)

def lese_gewicht():
    if USE_SIMULATION:
        return simuliere_gewicht()
    else:
        # Nur auf dem Raspberry Pi erlauben!
        if not sys.platform.startswith("linux") or "anaconda" in sys.executable.lower():
            print("Echtbetrieb nur auf Raspberry Pi möglich! Gebe 0 zurück.")
            return 0.0
        from hardware.hx711 import lese_gewicht_hx711
        return lese_gewicht_hx711()

def lese_einzelzellen():
    if USE_SIMULATION:
        return [round(random.uniform(0, 25), 2) for _ in range(4)]
    else:
        if not sys.platform.startswith("linux") or "anaconda" in sys.executable.lower():
            print("Echtbetrieb nur auf Raspberry Pi möglich! Gebe 0er-Liste zurück.")
            return [0.0, 0.0, 0.0, 0.0]
        from hardware.hx711 import lese_einzelzellwerte_hx711
        return lese_einzelzellwerte_hx711()

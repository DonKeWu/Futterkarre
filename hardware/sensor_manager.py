# hardware/sensor_manager.py
import hardware.hx711_sim as hx711_sim
import hardware.fu_sim as fu_sim
import sys


class SmartSensorManager:
    def read_weight(self) -> float:
        """Liest Gewicht: Simulation nur zum Testen, sonst echte Hardware"""

        if hx711_sim.USE_SIMULATION:
            # NUR zum Testen - simulierte Werte
            if fu_sim.USE_SIMULATION:
                return fu_sim.get_sim_weight()  # Fütterungssimulation
            else:
                import random
                return round(random.uniform(10, 100), 2)  # HX711-Simulation
        else:
            # PRODUKTIVBETRIEB - echte Hardware
            try:
                if sys.platform.startswith("linux") and "anaconda" not in sys.executable.lower():
                    # Auf Raspberry Pi - echte Hardware
                    from hardware.hx711_sensor import lese_gewicht_hx711
                    return lese_gewicht_hx711()
                else:
                    # Entwicklungsrechner - keine Hardware verfügbar
                    print("Warnung: Keine echte Hardware verfügbar (nicht auf Raspberry Pi)")
                    return 0.0
            except Exception as e:
                print(f"Fehler beim Lesen der echten Hardware: {e}")
                return 0.0

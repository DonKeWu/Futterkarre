# hardware/sensor_manager.py - VEREINFACHTE VERSION
import hardware.hx711_sim as hx711_sim
import sys

class SmartSensorManager:
    def read_weight(self) -> float:
        """Liest Gewicht: Simulation oder echte Hardware"""

        # Vereinfacht: Nur HX711-Simulation oder echte Hardware
        if hx711_sim.ist_simulation_aktiv():
            # Simulation aktiv - workflow-realistische Werte
            return hx711_sim.simuliere_gewicht()
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

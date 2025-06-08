# hardware/sensor_switch.py
from .hx711_real import HX711Sensor
from .hx711_sim import HX711SimSensor

class SensorManager:
    def __init__(self):
        self.use_simulation = False
        self._sensor = None

    @property
    def sensor(self):
        if not self._sensor:
            self._sensor = HX711SimSensor() if self.use_simulation else HX711Sensor(5, 6)
        return self._sensor

    def toggle_simulation(self, enable: bool):
        self.use_simulation = enable
        self._sensor = None  # Erzwingt Neuerstellung beim nächsten Zugriff

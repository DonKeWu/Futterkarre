from .sensor_interface import WeightSensorInterface

class HX711Sensor(WeightSensorInterface):
    def __init__(self, data_pin: int, clock_pin: int):
        # Initialisierung der HX711-Hardware (Pseudo-Code)
        self.data_pin = data_pin
        self.clock_pin = clock_pin

    def read_weight(self) -> float:
        # Hier würdest du die echte Bibliothek ansprechen, z.B. hx711python
        # return hx711.get_weight()
        return 2.5  # Dummywert für Beispiel

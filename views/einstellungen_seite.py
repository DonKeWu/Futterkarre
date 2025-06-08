# views/einstellungen_seite.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel


class EinstellungenSeite(QWidget):
    def __init__(self, sensor_manager, parent=None):
        super().__init__(parent)
        self.sensor_manager = sensor_manager
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Sensor-Simulation
        self.btn_sim = QPushButton("Sensor-Simulation")
        self.btn_sim.setCheckable(True)
        self.btn_sim.setChecked(self.sensor_manager.use_simulation)
        self.btn_sim.toggled.connect(self.sensor_manager.toggle_simulation)
        layout.addWidget(self.btn_sim)

        # Fütterungssimulation (Analog implementieren)
        # ...

        # Hardware-Status
        status = "Simulation" if self.sensor_manager.use_simulation else "Echtbetrieb"
        self.lbl_status = QLabel(f"Aktueller Modus: {status}")
        layout.addWidget(self.lbl_status)

        self.setLayout(layout)

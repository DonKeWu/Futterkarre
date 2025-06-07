from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self, sensor):
        super().__init__()
        self.sensor = sensor

        self.setWindowTitle("Futterkarre 2.0")
        self.setFixedSize(1024, 600)

        self.weight_label = QLabel("Gewicht: -- kg")
        self.refresh_button = QPushButton("Aktualisieren")

        layout = QVBoxLayout()
        layout.addWidget(self.weight_label)
        layout.addWidget(self.refresh_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.refresh_button.clicked.connect(self.update_weight)

        # Automatische Aktualisierung alle 1 Sekunde
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_weight)
        self.timer.start(1000)

    def update_weight(self):
        try:
            weight = self.sensor.read_weight()
            self.weight_label.setText(f"Gewicht: {weight:.2f} kg")
        except Exception as e:
            self.weight_label.setText("Fehler beim Wiegen!")
            # Hier könntest du ein Logging-Framework nutzen

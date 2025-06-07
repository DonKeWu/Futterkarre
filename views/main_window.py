# views/main_window.py

from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox
from PyQt5.QtCore import QTimer

class MainWindow(QMainWindow):
    def __init__(self, sensor, heu_namen=None):
        super().__init__()
        self.sensor = sensor

        self.setWindowTitle("Futterkarre 2.0")
        self.setFixedSize(1024, 600)

        # Gewichtsanzeige
        self.weight_label = QLabel("Gewicht: -- kg")
        self.refresh_button = QPushButton("Aktualisieren")

        # Dropdown für Heu-Auswahl
        self.combo_heu = QComboBox()
        if heu_namen is None:
            heu_namen = ["heu2024", "heu2025", "heu_nachbar2025"]
        self.combo_heu.addItems(heu_namen)
        self.combo_heu.currentIndexChanged.connect(self.on_heu_changed)

        layout = QVBoxLayout()
        layout.addWidget(self.weight_label)
        layout.addWidget(self.combo_heu)
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

    def on_heu_changed(self, index):
        heu_name = self.combo_heu.currentText()
        # Hier kannst du das neue Heu laden und ggf. anzeigen
        print(f"Aktuell ausgewähltes Heu: {heu_name}")

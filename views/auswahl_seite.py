from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from pathlib import Path

class AuswahlSeite(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = Path(__file__).parent / "auswahl.ui"
        uic.loadUi(str(ui_path), self)
        # Jetzt kannst du z.B. self.btn_heu.clicked.connect(...)

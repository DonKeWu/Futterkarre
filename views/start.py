import os
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

class StartSeite(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Ermittle den absoluten Pfad zur start.ui relativ zu diesem Skript
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_path = os.path.join(current_dir, 'start.ui')
        uic.loadUi(ui_path, self)


# main.py (Ausschnitt)

from config.logging_config import setup_logging
setup_logging()
import logging
logger = logging.getLogger(__name__)

import sys
import os

from config.app_config import AppConfig
from datetime import datetime
from models import Pferd, Heulage
from controllers.fuetterung_controller import FütterungController

from hardware.sensor_switch import SensorManager
from views.main_window import MainWindow
from utils.futter_loader import lade_heu_als_dataclasses

# Setze DPI/Skalierungs-Umgebungsvariablen VOR PyQt-Import!
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = AppConfig.QT_AUTO_SCREEN_SCALE_FACTOR
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = AppConfig.QT_ENABLE_HIGHDPI_SCALING
os.environ["QT_SCALE_FACTOR"] = AppConfig.QT_SCALE_FACTOR

from PyQt5 import QtWidgets, QtCore

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

from PyQt5.QtWidgets import QApplication

def main():
    sensor = HX711Sensor(data_pin=5, clock_pin=6)
    sensor_manager = SensorManager()
    heuliste = lade_heu_als_dataclasses("heu_eigen_2025.csv")
    heulage_liste = lade_heulage_als_dataclasses("heulage_eigen_2025.csv")
    pferde_liste = lade_pferde_als_dataclasses("pferde.csv")

    # 3. PyQt-Anwendung starten
    app = QApplication(sys.argv)
    # Übergib alle Listen an MainWindow, nicht nur Heu!
    window = MainWindow(sensor, heuliste=heuliste, heulage_liste=heulage_liste, pferde_liste=pferde_liste)
    window.show()
    sys.exit(app.exec_())

    # 4. Testdaten laden (optional/nur für Entwicklung)
    if True:
        pferd = Pferd(name="Blitz", gewicht=500, alter=8)
        heulage = Heulage(
            name="Heulage 2024", trockenmasse=60.0, rohprotein=14.0, rohfaser=24.0,
            gesamtzucker=8.0, fruktan=4.0, me_pferd=8.0, pcv_xp=7.0,
            herkunft="Hof B", jahrgang=2024, ph_wert=4.5, siliergrad="gut"
        )
        controller = FütterungController()
        controller.neue_fütterung(pferd, heulage, 2.5, datetime.now())

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

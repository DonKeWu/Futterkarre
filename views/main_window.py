# views/main_window.py
import logging
import views.icons.icons_rc
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import QTimer

from views.start import StartSeite
from views.fuettern_seite import FuetternSeite
from views.auswahl_seite import AuswahlSeite
from views.einstellungen_seite import EinstellungenSeite
from views.beladen_seite import BeladenSeite

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self, sensor_manager, heu_namen=None):
        super().__init__()
        self.sensor_manager = sensor_manager
        self.heu_namen = heu_namen if heu_namen is not None else []
        logger.info("MainWindow wird initialisiert")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Futterkarre 2.0")
        self.setFixedSize(1024, 600)

        self.stacked_widget = QStackedWidget()

        # Seiten anlegen - OHNE Parent-Verwirrung!
        self.start_screen = StartSeite()
        self.auswahl_seite = AuswahlSeite()
        self.beladen_seite = BeladenSeite(sensor_manager=self.sensor_manager)
        self.fuettern_seite = FuetternSeite()
        self.einstellungen_seite = EinstellungenSeite(sensor_manager=self.sensor_manager)

        # Navigation Manager für alle Seiten setzen -----------------------------------------------------------

        for seite in [self.start_screen, self.auswahl_seite, self.beladen_seite, self.fuettern_seite,
                      self.einstellungen_seite]:
            seite.navigation = self

        # Seiten zum Stack hinzufügen
        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.auswahl_seite)
        self.stacked_widget.addWidget(self.beladen_seite)
        self.stacked_widget.addWidget(self.fuettern_seite)
        self.stacked_widget.addWidget(self.einstellungen_seite)

        self.setCentralWidget(self.stacked_widget)
        self.show_status("start")
        self.connect_navigation()

    def connect_navigation(self):
        """Alle Seiten verwenden jetzt self.navigation - KEINE manuelle Verbindung nötig!"""
        pass

    def show_status(self, status, context=None):
        """Zentrale Navigation zwischen Seiten - JETZT mit Kontext!"""
        logger.info(f"Wechsel zu Status: {status}")

        # Timer stoppen bei Seitenwechsel - WICHTIG!
        self.stop_all_timers()

        if status == "start":
            self.stacked_widget.setCurrentWidget(self.start_screen)
        elif status == "auswahl":
            self.stacked_widget.setCurrentWidget(self.auswahl_seite)
        elif status == "beladen":
            self.stacked_widget.setCurrentWidget(self.beladen_seite)
            # WICHTIG: Kontext an Beladen-Seite übergeben
            if context:
                self.beladen_seite.set_context(context)
            self.beladen_seite.start_timer()  # Timer nur bei aktiver Seite
        elif status == "fuettern":
            self.stacked_widget.setCurrentWidget(self.fuettern_seite)
            # WICHTIG: Kontext an Füttern-Seite übergeben
            if context:
                self.fuettern_seite.restore_context(context)
        elif status == "einstellungen":
            self.stacked_widget.setCurrentWidget(self.einstellungen_seite)
            self.einstellungen_seite.start_timer()  # Timer nur bei aktiver Seite

    def stop_all_timers(self):
        """Stoppt alle Timer - verhindert Dauerschleifen"""
        if hasattr(self.beladen_seite, 'timer'):
            self.beladen_seite.timer.stop()
        if hasattr(self.einstellungen_seite, 'timer'):
            self.einstellungen_seite.timer.stop()

    # Einfache Navigation-Methoden
    def zeige_heu_futter(self):
        self.show_status("fuettern")

    def zeige_heulage_futter(self):
        self.show_status("fuettern")

    def zeige_futter_laden(self):
        self.show_status("beladen")

    def zeige_einstellungen(self):
        self.show_status("einstellungen")


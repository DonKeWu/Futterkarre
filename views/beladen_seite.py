# views/beladen_seite.py
import os
import views.icons.icons_rc
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer

class BeladenSeite(QWidget):
    def __init__(self, sensor_manager):
        super().__init__()
        self.sensor_manager = sensor_manager
        self.navigation = None  # Wird von MainWindow gesetzt

        # NEUE Kontext-Variablen
        self.context = {}
        self.restgewicht = 0.0
        self.pferd_nummer = 1
        self.aktuelles_pferd = None

        # UI laden (Ihr bestehender Code bleibt)
        ui_path = os.path.join(os.path.dirname(__file__), "beladen_seite.ui")
        if os.path.exists(ui_path):
            uic.loadUi(ui_path, self)
        else:
            self.create_ui_in_code()

        # Timer erstellen, aber NICHT starten
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_weight)

        # Navigation verbinden
        if hasattr(self, 'btn_beladen_abgeschlossen'):
            self.btn_beladen_abgeschlossen.clicked.connect(self.beladen_fertig)

    def set_context(self, context):
        """Empfängt Kontext von der Füttern-Seite"""
        self.context = context
        self.restgewicht = context.get('restgewicht', 0.0)
        self.pferd_nummer = context.get('pferd_nummer', 1)
        self.aktuelles_pferd = context.get('pferd_objekt', None)

        logger.info(
            f"Beladen-Seite: Kontext erhalten - Pferd {self.pferd_nummer}, Restgewicht: {self.restgewicht:.2f} kg")

        # Status-Label aktualisieren
        if hasattr(self, 'label_status'):
            self.label_status.setText(f"Nachladen für Pferd {self.pferd_nummer}")

    def beladen_fertig(self):
        """Navigation zurück zur Füttern-Seite MIT Kontext"""
        if self.navigation:
            # Kontext mit aktuellem Gewicht zurückgeben
            aktuelles_gewicht = self.sensor_manager.read_weight()
            self.context['neues_gewicht'] = aktuelles_gewicht
            self.context['nachgeladen'] = aktuelles_gewicht - self.restgewicht

            logger.info(f"Beladen abgeschlossen: {self.context['nachgeladen']:.2f} kg nachgeladen")
            self.navigation.show_status("fuettern", self.context)

    def update_weight(self):
        try:
            aktuelles_gewicht = self.sensor_manager.read_weight()

            # Hauptanzeige aktualisieren
            if hasattr(self, 'label_hauptgewicht'):
                self.label_hauptgewicht.setText(f"{aktuelles_gewicht:.2f} kg")
            if hasattr(self, 'label_aktuelles_gewicht'):
                self.label_aktuelles_gewicht.setText(f"Aktuelles Gewicht: {aktuelles_gewicht:.2f} kg")

            # Nachgeladene Menge berechnen
            if self.restgewicht > 0:
                nachgeladen = aktuelles_gewicht - self.restgewicht
                if hasattr(self, 'label_nachgeladen'):
                    self.label_nachgeladen.setText(f"Nachgeladen: {nachgeladen:.1f} kg")

                # Button aktivieren wenn genug nachgeladen
                if hasattr(self, 'btn_beladen_abgeschlossen'):
                    if nachgeladen > 5.0:  # Mindestens 5kg nachgeladen
                        self.btn_beladen_abgeschlossen.setEnabled(True)
                        self.btn_beladen_abgeschlossen.setStyleSheet("background-color: #4CAF50;")
                    else:
                        self.btn_beladen_abgeschlossen.setEnabled(False)
                        self.btn_beladen_abgeschlossen.setStyleSheet("background-color: #CCCCCC;")

        except Exception as e:
            logger.error(f"Fehler beim Wiegen: {e}")
            if hasattr(self, 'label_hauptgewicht'):
                self.label_hauptgewicht.setText("Fehler!")

# views/fuettern_seite.py

import views.icons.icons_rc
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup
from PyQt5.QtCore import Qt

class FuetternSeite(QWidget):
    def __init__(self, pferd=None, parent=None):
        super().__init__(parent)
        self.navigation = None  # Wird von MainWindow gesetzt
        self.pferd = pferd
        self.create_ui()
        self.connect_buttons()
        # NEUE Kontext-Variablen
        self.aktuelle_pferd_nummer = 1
        self.aktuelles_pferd = None
        self.letztes_gewicht = 0.0

        self.create_ui()
        self.connect_buttons()

    def create_ui(self):
        # Ihr bestehender UI-Code bleibt gleich
        main_layout = QVBoxLayout()
        futterart_layout = QHBoxLayout()
        navigation_layout = QHBoxLayout()

        # Pferdeanzeige
        self.label_pferd = QLabel("Kein Pferd gewählt")
        self.label_pferd.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_pferd)

        # Futterart-Schalter
        self.futterart_group = QButtonGroup(self)
        self.futterart_buttons = {}
        futterarten = ["Heu", "Heulage", "Kraftfutter", "Hafer"]
        for i, art in enumerate(futterarten):
            btn = QPushButton(art)
            btn.setCheckable(True)
            btn.setMinimumHeight(80)
            btn.setMinimumWidth(180)
            if i == 0:
                btn.setChecked(True)
            self.futterart_group.addButton(btn, i)
            self.futterart_buttons[art] = btn
            futterart_layout.addWidget(btn)
        main_layout.addLayout(futterart_layout)

        # Gewichtsanzeige
        self.label_gewicht = QLabel("Gewicht: -- kg")
        self.label_gewicht.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.label_gewicht)

        # Navigationsbuttons
        self.btn_nachladen = QPushButton("Nachladen")
        self.btn_fuettern = QPushButton("Füttern")
        self.btn_naechstes_pferd = QPushButton("Nächstes Pferd")
        self.btn_nachladen.setMinimumHeight(60)
        self.btn_fuettern.setMinimumHeight(60)
        self.btn_naechstes_pferd.setMinimumHeight(60)
        navigation_layout.addWidget(self.btn_nachladen)
        navigation_layout.addWidget(self.btn_fuettern)
        navigation_layout.addWidget(self.btn_naechstes_pferd)
        main_layout.addLayout(navigation_layout)

        self.setLayout(main_layout)

    def connect_buttons(self):
        """Verbindet alle Buttons mit Navigation"""
        self.futterart_group.buttonClicked.connect(self.futterart_gewaehlt)
        self.btn_fuettern.clicked.connect(self.fuettern)
        self.btn_nachladen.clicked.connect(self.nachladen_mit_kontext)  # GEÄNDERT!
        self.btn_naechstes_pferd.clicked.connect(self.naechstes_pferd)

    def futterart_gewaehlt(self, button):
        print(f"Futterart gewählt: {button.text()}")

    def fuettern(self):
        print("Fütterung bestätigt!")

    def zu_beladen(self):
        if self.navigation:
            self.navigation.show_status("beladen")

    def zu_start(self):
        if self.navigation:
            self.navigation.show_status("start")

    def setze_pferd(self, pferd):
        self.pferd = pferd
        self.label_pferd.setText(f"{pferd.name} ({pferd.gewicht} kg)")

    def nachladen_mit_kontext(self):
        """Nachladen mit Kontext-Erhaltung"""
        # Aktuellen Zustand speichern
        context = {
            'pferd_nummer': self.aktuelle_pferd_nummer,
            'pferd_objekt': self.aktuelles_pferd,
            'restgewicht': self.letztes_gewicht,
            'von_seite': 'fuettern'
        }

        logger.info(f"Nachladen: Speichere Kontext für Pferd {self.aktuelle_pferd_nummer}")

        if self.navigation:
            self.navigation.show_status("beladen", context)

    def restore_context(self, context):
        """Stellt Kontext nach dem Beladen wieder her"""
        self.aktuelle_pferd_nummer = context.get('pferd_nummer', 1)
        self.aktuelles_pferd = context.get('pferd_objekt', None)
        nachgeladen = context.get('nachgeladen', 0.0)

        logger.info(
            f"Füttern-Seite: Kontext wiederhergestellt - Pferd {self.aktuelle_pferd_nummer}, nachgeladen: {nachgeladen:.2f} kg")

        # UI aktualisieren
        if self.aktuelles_pferd:
            self.setze_pferd(self.aktuelles_pferd)

        # Erfolgsmeldung anzeigen
        if hasattr(self, 'label_status'):
            self.label_status.setText(f"Karre nachgeladen: +{nachgeladen:.1f} kg")

    def naechstes_pferd(self):
        """Zum nächsten Pferd wechseln"""
        self.aktuelle_pferd_nummer += 1
        # Hier würden Sie das nächste Pferd laden
        logger.info(f"Wechsel zu Pferd {self.aktuelle_pferd_nummer}")

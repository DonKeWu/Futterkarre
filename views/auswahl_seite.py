# views/auswahl_seite.py
import os
import sys
import logging
import views.icons.icons_rc

# Basis-Widget importieren
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.base_ui_widget import BaseViewWidget

logger = logging.getLogger(__name__)


class AuswahlSeite(BaseViewWidget):
    def __init__(self, parent=None):
        # BaseViewWidget mit UI-Datei initialisieren  
        super().__init__(parent, ui_filename="auswahl_seite.ui", page_name="auswahl")
        
        # Spezielle Buttons verbinden
        self.connect_buttons()

    def connect_buttons(self):
        """Verbindet Buttons nach UI-Laden"""
        if hasattr(self, 'btn_to_side_fu_heu'):
            self.btn_to_side_fu_heu.clicked.connect(self.zu_heu_futter)
        if hasattr(self, 'btn_to_side_fu_heulage'):
            self.btn_to_side_fu_heulage.clicked.connect(self.zu_heulage_futter)
        if hasattr(self, 'btn_to_side_fu_laden'):
            self.btn_to_side_fu_laden.clicked.connect(self.zu_beladen)
        if hasattr(self, 'btn_to_side_settings'):
            self.btn_to_side_settings.clicked.connect(self.zu_einstellungen)

        logger.info("AuswahlSeite Buttons verbunden")

    def zu_heu_futter(self):
        if self.navigation:
            if hasattr(self.navigation, "zeige_heu_futter"):
                self.navigation.zeige_heu_futter()
            else:
                self.navigation.show_status("fuettern")

    def zu_heulage_futter(self):
        if self.navigation:
            if hasattr(self.navigation, "zeige_heulage_futter"):
                self.navigation.zeige_heulage_futter()
            else:
                self.navigation.show_status("fuettern")

    def zu_beladen(self):
        if self.navigation:
            self.navigation.show_status("beladen")

    def zu_einstellungen(self):
        if self.navigation:
            self.navigation.show_status("einstellungen")

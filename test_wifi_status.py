#!/usr/bin/env python3
"""
Test für WiFi Status Integration in FütternSeite
Testet ESP8266 Auto-Discovery und Status-Anzeige
"""
import sys
import os

# Pfad zum Projekt hinzufügen
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from views.fuettern_seite import FuetternSeite
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_wifi_status():
    """Testet WiFi Status Integration"""
    app = QApplication(sys.argv)
    
    # FütternSeite erstellen
    fuettern_seite = FuetternSeite()
    fuettern_seite.show()
    
    logger.info("WiFi Status Test gestartet")
    logger.info("- Grüner Rahmen = ESP8266 verbunden")
    logger.info("- Grauer Rahmen = ESP8266 nicht erreichbar")
    logger.info("- Tooltip zeigt ESP8266 IP-Adresse bei Verbindung")
    
    # GUI starten
    return app.exec_()

if __name__ == "__main__":
    test_wifi_status()
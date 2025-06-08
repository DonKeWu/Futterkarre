# config/app_config.py
import logging
logger = logging.getLogger(__name__)

class AppConfig:
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 600
    TIMER_INTERVAL_MS = 1000
    DATA_PATH = "data/"
    BG_COLOR = "#fdffe0"  # Hintergrundfarbe als Konstante

    # DPI/Skalierungs-Settings als Strings (nur als Info, nicht ausführen!)
    QT_AUTO_SCREEN_SCALE_FACTOR = "1"
    QT_ENABLE_HIGHDPI_SCALING = "1"
    QT_SCALE_FACTOR = "1"


# config/app_config.py
class AppConfig:
    # Display-Einstellungen für PyQt5
    QT_AUTO_SCREEN_SCALE_FACTOR = "1"
    QT_ENABLE_HIGHDPI_SCALING = "1"
    QT_SCALE_FACTOR = "1.0"

    # Debug-Modus - FEHLTE!
    DEBUG_MODE = True

    # Hardware-Einstellungen
    USE_HARDWARE_SIMULATION = True

    # Logging-Level
    LOG_LEVEL = "INFO"

    # Pfade
    DATA_PATH = "data/"
    LOGS_PATH = "logs/"

    # UI-Einstellungen
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 600
    TOUCH_OPTIMIZED = True



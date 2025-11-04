# config/app_config.py
class AppConfig:
    # Display-Einstellungen für PyQt5
    QT_AUTO_SCREEN_SCALE_FACTOR = "1"
    QT_ENABLE_HIGHDPI_SCALING = "1"
    QT_SCALE_FACTOR = "0.78"  # 800/1024 = 0.78125 für Raspberry Pi Touch Display

    # Debug-Modus - FEHLTE!
    DEBUG_MODE = True

    # Hardware-Einstellungen
    USE_HARDWARE_SIMULATION = True

    # Logging-Level
    LOG_LEVEL = "INFO"

    # Pfade
    DATA_PATH = "data/"
    LOGS_PATH = "logs/"

    # UI-Einstellungen - Raspberry Pi Touch Display
    WINDOW_WIDTH = 800   # Raspberry Pi Touch Display
    WINDOW_HEIGHT = 480  # Raspberry Pi Touch Display 
    TOUCH_OPTIMIZED = True



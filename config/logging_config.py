# config/logging_config.py
import logging
import os


def setup_logging():
    # logs-Ordner erstellen falls nicht vorhanden
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),  # Konsolen-Ausgabe (wie bisher)
            logging.FileHandler(os.path.join(log_dir, "futterkarre.log")),  # Datei-Ausgabe
            logging.FileHandler(os.path.join(log_dir, "debug.log"))  # Zusätzliche Debug-Datei
        ]
    )



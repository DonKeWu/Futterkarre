# utils/validation.py
import logging

logger = logging.getLogger(__name__)

def validate_pferd(pferd: dict) -> bool:
    """Validiert die wichtigsten Felder eines Pferds."""
    required_fields = ['Name', 'Gewicht', 'Alter']
    for field in required_fields:
        if field not in pferd:
            logger.error(f"Fehlendes Feld in Pferdedaten: {field}")
            return False
    if not isinstance(pferd['Gewicht'], (int, float)) or pferd['Gewicht'] <= 0:
        logger.error(f"Ungültiges Gewicht: {pferd['Gewicht']}")
        return False
    if not isinstance(pferd['Alter'], int) or pferd['Alter'] <= 0:
        logger.error(f"Ungültiges Alter: {pferd['Alter']}")
        return False
    return True

def validate_heu(heu: dict) -> bool:
    required_fields = ['Trockensubstanz', 'Rohprotein', 'Rohfaser', 'Gesamtzucker', 'Fruktan', 'ME-Pferd']
    for field in required_fields:
        if field not in heu or heu[field] == "":
            logger.error(f"Fehlendes Feld in Heudaten: {field}")
            return False
    return True

def validate_heulage(heulage: dict) -> bool:
    required_fields = ['Trockensubstanz', 'Rohprotein', 'Rohfaser', 'Gesamtzucker', 'Fruktan', 'ME-Pferd']
    for field in required_fields:
        if field not in heulage or heulage[field] == "":
            logger.error(f"Fehlendes Feld in Heulagedaten: {field}")
            return False
    return True
# utils/validation.py
import logging

logger = logging.getLogger(__name__)

def validate_pferd(pferd: dict) -> bool:
    """Validiert die wichtigsten Felder eines Pferds."""
    # Für leere Boxen ist Name optional
    aktiv = pferd.get('Aktiv', 'true').lower() == 'true'
    
    if not aktiv:
        # Leere Box - nur Box-Nummer erforderlich
        return 'Box' in pferd or 'Folge' in pferd
    
    # Aktive Pferde benötigen alle Felder
    required_fields = ['Name', 'Gewicht', 'Alter']
    for field in required_fields:
        if field not in pferd or not pferd[field]:
            logger.error(f"Fehlendes Feld in Pferdedaten: {field}")
            return False
            
    try:
        gewicht = float(pferd['Gewicht'])
        alter = int(pferd['Alter'])
        if gewicht <= 0 or alter <= 0:
            logger.error(f"Ungültige Werte: Gewicht={gewicht}, Alter={alter}")
            return False
    except (ValueError, TypeError):
        logger.error(f"Konvertierungsfehler bei Pferdedaten: {pferd}")
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
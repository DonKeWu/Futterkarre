from typing import List
from models import Fütterung, Pferd, Futter
from datetime import datetime

class FütterungController:
    def __init__(self):
        self.fütterungen: List[Fütterung] = []

    def neue_fütterung(self, pferd: Pferd, futter: Futter, menge_kg: float, zeitpunkt: datetime):
        # Dummy-Nährwertberechnung
        naehrwerte = {
            "Rohprotein": futter.rohprotein * menge_kg,
            "Rohfaser": futter.rohfaser * menge_kg,
        }
        fütterung = Fütterung(
            pferd=pferd,
            futter=futter,
            menge_kg=menge_kg,
            naehrwerte=naehrwerte,
            zeitpunkt=zeitpunkt
        )
        self.fütterungen.append(fütterung)
        return fütterung

from dataclasses import dataclass
from typing import Optional, Dict
from datetime import datetime
from .pferd import Pferd
from .futter import Futter

@dataclass
class Fütterung:
    pferd: Pferd
    futter: Futter
    menge_kg: float
    naehrwerte: Optional[Dict[str, float]] = None
    zeitpunkt: Optional[datetime] = None

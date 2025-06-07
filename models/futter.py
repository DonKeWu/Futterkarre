from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class Futter:
    name: str
    trockenmasse: float
    rohprotein: float
    rohfaser: float
    gesamtzucker: float
    fruktan: float
    me_pferd: float
    pcv_xp: float
    herkunft: Optional[str] = None
    jahrgang: Optional[int] = None

@dataclass
class Heu(Futter):
    staubarm: Optional[bool] = None

@dataclass
class Heulage(Futter):
    ph_wert: Optional[float] = None
    siliergrad: Optional[str] = None

@dataclass
class PelletFutter(Futter):
    zusatzstoffe: Optional[Dict[str, float]] = None

@dataclass
class Hafer(Futter):
    sorte: Optional[str] = None
    stärke: Optional[float] = None

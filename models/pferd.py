from dataclasses import dataclass
from typing import Optional

@dataclass
class Pferd:
    name: str
    gewicht: float
    alter: int
    box: int
    aktiv: bool = True
    notizen: Optional[str] = None

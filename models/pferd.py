from dataclasses import dataclass
from typing import Optional

@dataclass
class Pferd:
    name: str
    gewicht: float
    alter: int
    notizen: Optional[str] = None

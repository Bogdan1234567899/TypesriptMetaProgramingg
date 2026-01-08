from dataclasses import dataclass
from typing import Dict

@dataclass
class PsychologicalResult:
    user_id: int
    taken_at: str
    scores: Dict[str, int]
    average: float

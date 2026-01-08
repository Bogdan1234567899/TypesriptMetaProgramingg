from dataclasses import dataclass

@dataclass
class FinanceRecord:
    user_id: int
    amount: float
    category: str
    description: str

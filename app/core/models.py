from dataclasses import dataclass
from typing import Optional


@dataclass
class Transaction:
    id: str
    amount: float
    category: str
    date: str
    currency: Optional[str] = "USD"

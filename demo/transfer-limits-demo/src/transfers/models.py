from dataclasses import dataclass, field
from decimal import Decimal
from datetime import datetime


@dataclass
class Account:
    id: str
    currency: str          # ISO 4217, например "RUB"
    balance: Decimal


@dataclass
class Transfer:
    id: str
    src_account: str
    dst_account: str
    amount: Decimal
    currency: str
    created_at: datetime = field(default_factory=datetime.utcnow)

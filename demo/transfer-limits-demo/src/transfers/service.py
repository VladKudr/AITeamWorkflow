"""Сервис внутрибанковских переводов между счетами."""
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from .models import Account, Transfer
from .errors import InsufficientFunds, CurrencyMismatch, InvalidAmount, DailyLimitExceeded


class TransferService:
    def __init__(self, daily_limit: Decimal | None = None):
        """daily_limit — суточный лимит суммы переводов со счёта (календарные
        сутки UTC); None — проверка лимита отключена."""
        self._transfers: list[Transfer] = []
        self._daily_limit = daily_limit

    def create_transfer(self, src: Account, dst: Account, amount: Decimal) -> Transfer:
        if amount <= 0:
            raise InvalidAmount(f"Сумма перевода должна быть положительной, получено: {amount}")
        if src.currency != dst.currency:
            raise CurrencyMismatch(
                f"Валюты счетов не совпадают: {src.currency} != {dst.currency}"
            )
        if src.balance < amount:
            raise InsufficientFunds(
                f"Недостаточно средств: баланс {src.balance}, требуется {amount}"
            )
        if self._daily_limit is not None:
            spent = self._spent_today(src.id)
            if spent + amount > self._daily_limit:
                raise DailyLimitExceeded(
                    f"Превышен суточный лимит {self._daily_limit}: "
                    f"израсходовано {spent}, запрошено {amount}"
                )
        src.balance -= amount
        dst.balance += amount
        transfer = Transfer(
            id=str(uuid.uuid4()),
            src_account=src.id,
            dst_account=dst.id,
            amount=amount,
            currency=src.currency,
        )
        self._transfers.append(transfer)
        return transfer

    def _spent_today(self, account_id: str) -> Decimal:
        """Сумма успешных переводов со счёта за текущие календарные сутки (UTC)."""
        today = datetime.now(timezone.utc).date()
        return sum(
            (t.amount for t in self._transfers
             if t.src_account == account_id
             and t.created_at.replace(tzinfo=timezone.utc).date() == today),
            Decimal("0"),
        )

    def transfers_of(self, account_id: str) -> list[Transfer]:
        return [t for t in self._transfers if t.src_account == account_id]

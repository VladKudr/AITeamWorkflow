from decimal import Decimal
import pytest
from src.transfers.models import Account
from src.transfers.service import TransferService
from src.transfers.errors import InsufficientFunds, CurrencyMismatch, InvalidAmount


def acc(id="a1", currency="RUB", balance="1000"):
    return Account(id=id, currency=currency, balance=Decimal(balance))


def test_successful_transfer_moves_money():
    s, d = acc(), acc(id="a2", balance="0")
    svc = TransferService()
    t = svc.create_transfer(s, d, Decimal("100"))
    assert s.balance == Decimal("900") and d.balance == Decimal("100")
    assert t.currency == "RUB"


def test_rejects_non_positive_amount():
    svc = TransferService()
    with pytest.raises(InvalidAmount):
        svc.create_transfer(acc(), acc(id="a2"), Decimal("0"))


def test_rejects_currency_mismatch():
    svc = TransferService()
    with pytest.raises(CurrencyMismatch):
        svc.create_transfer(acc(), acc(id="a2", currency="USD"), Decimal("10"))


def test_rejects_insufficient_funds():
    svc = TransferService()
    with pytest.raises(InsufficientFunds):
        svc.create_transfer(acc(balance="50"), acc(id="a2"), Decimal("100"))


# --- Тесты по test-model.md change'а add-daily-transfer-limit ---
from datetime import timedelta, datetime
from src.transfers.errors import DailyLimitExceeded


def test_tc01_rejects_transfer_over_daily_limit():
    svc = TransferService(daily_limit=Decimal("1000"))
    s, d = acc(balance="5000"), acc(id="a2", balance="0")
    svc.create_transfer(s, d, Decimal("900"))
    with pytest.raises(DailyLimitExceeded):
        svc.create_transfer(s, d, Decimal("200"))
    assert s.balance == Decimal("4100")  # баланс после отказа не изменился


def test_tc02_exact_remaining_limit_passes():
    svc = TransferService(daily_limit=Decimal("1000"))
    s, d = acc(balance="5000"), acc(id="a2", balance="0")
    svc.create_transfer(s, d, Decimal("900"))
    t = svc.create_transfer(s, d, Decimal("100"))
    assert t.amount == Decimal("100")


def test_tc03_limit_resets_on_new_day():
    svc = TransferService(daily_limit=Decimal("1000"))
    s, d = acc(balance="5000"), acc(id="a2", balance="0")
    t = svc.create_transfer(s, d, Decimal("1000"))
    t.created_at = datetime.utcnow() - timedelta(days=1)  # перевод «вчера»
    assert svc.create_transfer(s, d, Decimal("500")).amount == Decimal("500")


def test_tc04_no_limit_configured_disables_check():
    svc = TransferService()
    s, d = acc(balance="999999"), acc(id="a2", balance="0")
    assert svc.create_transfer(s, d, Decimal("999999")).amount == Decimal("999999")


def test_tc05_insufficient_funds_checked_before_limit():
    svc = TransferService(daily_limit=Decimal("1000"))
    with pytest.raises(InsufficientFunds):
        svc.create_transfer(acc(balance="50"), acc(id="a2"), Decimal("100"))

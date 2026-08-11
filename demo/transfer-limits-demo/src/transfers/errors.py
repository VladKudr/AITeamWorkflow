class TransferError(Exception):
    """Базовая ошибка перевода."""
    code = "TRANSFER_ERROR"


class InsufficientFunds(TransferError):
    code = "INSUFFICIENT_FUNDS"


class CurrencyMismatch(TransferError):
    code = "CURRENCY_MISMATCH"


class InvalidAmount(TransferError):
    code = "INVALID_AMOUNT"


class DailyLimitExceeded(TransferError):
    code = "DAILY_LIMIT_EXCEEDED"

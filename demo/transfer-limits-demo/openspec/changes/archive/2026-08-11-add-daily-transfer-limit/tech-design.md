# Tech Design: Суточный лимит переводов

## Подход
Реализация solution-design в терминах кодовой базы: расчёт суточной суммы по
self._transfers, проверка в create_transfer после существующих валидаций.

## Изменяемые модули и файлы
- `src/transfers/errors.py` — новая ошибка DailyLimitExceeded (code DAILY_LIMIT_EXCEEDED)
- `src/transfers/service.py` — параметр daily_limit в TransferService.__init__;
  метод _spent_today(account_id); проверка лимита в create_transfer
- `tests/test_transfers.py` — тесты по тест-модели

## Зависимости и миграции
Нет. Стандартная библиотека (datetime, Decimal).

## Отклонения от solution-design
Нет.

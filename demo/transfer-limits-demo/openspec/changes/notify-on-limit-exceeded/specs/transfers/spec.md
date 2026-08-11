# Delta for Transfers

## ADDED Requirements

### Requirement: Событие о превышении суточного лимита
Система SHALL публиковать событие limit_exceeded при отклонении перевода с
ошибкой DAILY_LIMIT_EXCEEDED, включая идентификатор счёта, сумму отклонённого
перевода и остаток лимита.

#### Scenario: Событие при отказе по лимиту
- GIVEN лимит 1000 RUB и израсходовано 900 RUB за сутки
- WHEN создаётся перевод на 200 RUB
- THEN перевод отклоняется с ошибкой DAILY_LIMIT_EXCEEDED
- AND публикуется событие limit_exceeded со счётом, суммой 200 и остатком 100

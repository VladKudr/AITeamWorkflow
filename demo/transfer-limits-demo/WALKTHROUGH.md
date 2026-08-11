# WALKTHROUGH: полный цикл SDD-workflow на живом примере

Этот репозиторий — демонстрация playbook'а (схема sdd-roles) от интент-брифа
до archive. Всё здесь настоящее: артефакты созданы по шаблонам схемы, спеки
проверены `openspec validate --strict`, код покрыт тестами из тест-модели,
дельта влита в main spec командой `openspec archive`. История git повторяет
командную конвенцию «один change — одна ветка — один PR».

Демо-задача: к сервису переводов добавить **суточный лимит переводов со счёта**.

## Как читать демо

Смотрите историю: `git log --oneline --graph`. Четыре точки:

1. `Начальное состояние` — сервис переводов ДО цикла (базовые проверки, 4 теста).
2. `openspec init + main spec` — подключение OpenSpec и baseline (сценарий А
   playbook: main spec наполнен и подписан СА до старта изменений).
3. `PR: add-daily-transfer-limit` — весь change одним PR: артефакты + код + тесты.
4. В merge-коммите — archive: дельта влита в `openspec/specs/transfers/spec.md`.

Второй change `notify-on-limit-exceeded` намеренно оставлен «в полёте» (2/6
артефактов) — чтобы посмотреть, как выглядит работа в процессе:
`openspec status --change notify-on-limit-exceeded` показывает, что tech-design
заблокирован до появления solution-design.

## Цикл по шагам (кто → команда → артефакт → гейт)

### Шаг 0 · PM · интент-бриф (гейт G0)
Файл: `docs/intent-brief-add-daily-transfer-limit.md`.
PM заполняет шаблон в чат-LLM, CLI не использует. Обратите внимание на секции
«НЕ в этом изменении» и «Что обидно сломать» — из них дальше вырастут
границы scope и граничные сценарии спеки.

### Шаг 1 · СА · change + proposal (гейт G1 — подпись PM)
В GigaCode: `/opsx-new add-daily-transfer-limit`, затем `/opsx-continue`.
Файл: `openspec/changes/archive/2026-08-11-add-daily-transfer-limit/proposal.md`.
Ссылка на бриф обязательна (правило схемы). Rollback-план — через конфигурацию,
без отката кода.

### Шаг 2 · СА · дельта спеки (гейт G2 — validate + QA о тестируемости)
В GigaCode: `/opsx-continue`. Файл: `…/specs/transfers/spec.md` (в архиве).
Дельта — `## ADDED Requirements`: одно требование, ЧЕТЫРЕ сценария — негатив,
граница («ровно в остаток лимита» из брифа PM!), сброс суток, выключенный лимит.
Проверка: `openspec validate add-daily-transfer-limit --strict` → valid.

### Шаг 3 · СА · solution-design (гейт G3a)
Файл: `…/solution-design.md`. Уровень СА: алгоритм расчёта суточной суммы,
решение «считать по журналу, а не вести счётчик» с альтернативами, порядок
проверок, календарные сутки UTC. Кода и имён файлов нет.

### Шаг 4 · Dev · tech-design (гейт G3b — СА сверяет с solution-design)
Файл: `…/tech-design.md`. Тот же замысел в терминах кодовой базы: какие файлы
меняются, каким методом. Раздел «Отклонения от solution-design: нет» — это
предмет проверки гейта.

### Шаг 5 · QA · тест-модель (параллельно шагу 4)
Файл: `…/test-model.md`. Построена ИЗ СЦЕНАРИЕВ спеки, не из кода: TC-01…TC-04
трассируются на сценарии требования, TC-05 — регресс требования из main spec
(порядок проверок). Кейс «граница» приоритетом high — прямо из «что обидно
сломать».

### Шаг 6 · Dev · tasks + реализация (гейт G4 — PR)
В GigaCode: `/opsx-continue` (tasks), затем `/opsx-apply`.
Файлы: `…/tasks.md` (все отмечены), код: `src/transfers/errors.py`,
`src/transfers/service.py`. PR содержит спеку И код — ревью в порядке
proposal → дельта → код.

### Шаг 7 · QA · верификация (гейт G5)
Тесты из тест-модели: `tests/test_transfers.py` (блок TC-01…TC-05).
`python -m pytest -q` → 9 passed. В боевом цикле здесь же `/opsx-verify`.

### Шаг 8 · СА · archive (гейт G6 — после мерджа PR)
`openspec archive add-daily-transfer-limit --yes` →
дельта влита: в `openspec/specs/transfers/spec.md` теперь 5 требований
(было 4), change уехал в `openspec/changes/archive/2026-08-11-…/` целиком.
Main spec снова описывает актуальное поведение — следующий change
(notify-on-limit-exceeded) уже ссылается на требование лимита как на данность.

## Что проверить руками (5 минут)

```sh
python -m pytest -q                                  # 9 passed
openspec list --specs                                # capability transfers
openspec validate --all --strict                     # всё valid
openspec status --change notify-on-limit-exceeded    # механика блокировок схемы
git log --oneline --graph                            # конвенция change=ветка=PR
```

## Чему учит демо

- Дельта против main spec: требование лимита появилось как ADDED и стало
  частью источника истины только после archive.
- Схема sdd-roles реально ведёт порядок артефактов: см. блокировки в статусе
  второго change'а.
- Тест-модель из спеки, а не из кода: TC-05 ловит порядок проверок, который
  зафиксирован в solution-design, а граничный TC-02 родился из брифа PM.
- Один PR = спека + код: ревьюеру не нужно восстанавливать замысел по диффу.

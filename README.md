# AITeamWorkflow

Единый SDD-workflow команды (PM · системный аналитик · разработчик · QA) на базе
OpenSpec и GigaCode: роли, артефакты, гейты, команды — и живой пример полного цикла.

## Состав

| Путь | Что это |
|---|---|
| [`docs/index.html`](docs/index.html) | **SDD Playbook** — полный документ: workflow, роли, RACI, гейты, команды, демо. Открыть в браузере; печать даёт чистую версию |
| [`starter-pack/`](starter-pack/) | Стартовый пакет для репозитория: схема `sdd-roles`, `config.yaml`, шаблоны артефактов, шаблон интент-брифа |
| [`demo/transfer-limits-demo/`](demo/transfer-limits-demo/) | Демо-проект: полный цикл playbook, реально пройденный на мини-сервисе переводов. Маршрут — `WALKTHROUGH.md` |
| `demo/transfer-limits-demo-with-git-history.zip` | Тот же демо-проект с git-историей (конвенция change = ветка = PR видна в `git log --graph`) |

## Быстрый старт

1. Прочитать playbook (`docs/index.html`).
2. Пройти демо: распаковать zip с историей, `python -m pytest -q`, `git log --oneline --graph`, `WALKTHROUGH.md`.
3. Подключить workflow в своём репозитории: `openspec init --tools qwen`, скопировать `starter-pack/`.

Упражнение первого занятия: довести change `notify-on-limit-exceeded` в демо до archive.

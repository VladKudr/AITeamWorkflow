# Стартовый пакет: SDD-workflow (OpenSpec + Qwen Code)

Содержимое кладётся в корень репозитория ПОСЛЕ `openspec init --tools qwen`:

```
openspec/config.yaml                      — конфигурация проекта (схема, context, rules)
openspec/schemas/sdd-roles/schema.yaml    — кастомная схема workflow под роли
openspec/schemas/sdd-roles/templates/     — шаблоны артефактов
docs/intent-brief-template.md             — шаблон интент-брифа (артефакт PM)
```

Проверка после установки:

```
openspec schema validate sdd-roles
openspec schemas          # sdd-roles должна быть в списке
openspec validate --all --strict
```

Подробности — в SDD Playbook (html-документ рядом с этим архивом).

# Implementation Strategy

- Хранить диаграммы в Markdown с Mermaid-блоками.
- Использовать GitHub/GitLab для рендеринга Mermaid или внешний рендерер в CI.
- Собираемый процесс (ATCG) парсит `core/honey.md` и по `@include` собирает итоговый документ.
- Возможно: программная генерация Mermaid из метаданных (Python скрипты).
- Рекомендация: добавить linting для `core/honey.md` (проверка ссылок и порядка).

# Структура проекта (Обновлено 2026-03-13)

Все файлы организованы по функциональному назначению для удобства навигации.

## 📁 Документация (`docs/`)
- `google-antigravity.md` — Документация по платформе Google Antigravity.
- `kimi-k2.5.md` — Описание возможностей модели Kimi K2.5.
- `telegram_bot_beget_guide.md` — Руководство по развертыванию ботов.

## 📁 Проекты (`projects/`)
Основные рабочие проекты вынесены в отдельную папку:
- `invite_bot_new/` — Бот для отслеживания приглашений.
- `n8n_daily_messages/` — Автоматизация ежедневных отчетов в n8n.
- `personal_agent/` — Персональный AI-агент (включая рыболовный агент).
- `portfolio/` — Портфолио и кейсы проектов.
- `superagent/` — Воркфлоу для n8n и гайды по Salebot.
- `telegram-analytics-saas/` — SaaS платформа для аналитики Telegram.

## 📁 Скрипты и Код (Организовано)

### 📂 JavaScript (`js/`)
- `parsers/` — Парсеры JSON и табличных данных.
- `aggregators/` — Агрегация нод и кода.
- `formatters/` — Форматирование отчетов и текста.
- `solutions/` — Основные решения и рабочие скрипты.
- `debug_and_fixes/` — Скрипты для отладки и быстрых исправлений.
- `managers/` — Данные по менеджерам.

### 📂 Скрипты (`scripts/`)
- `automation/` — Автоматизация через Expect (.exp) для SSH и команд.
- `maintenance/` — Обслуживание, бэкапы и исправления (Bash, Python).
- `reports/` — Генерация ежедневных и персональных отчетов (Python).
- `tests/` — Тесты для ботов, воркфлоу и запросов.
- `setup/` — Скрипты установки и настройки сервисов.

### 📂 SQL Запросы (`sql/`)
- `funnels/` — Анализ воронок продаж.
- `clients/` — Работа с клиентскими данными.
- `reports/` — Отчеты по менеджерам и общие отчеты.
- `json_helpers/` — Вспомогательные запросы для работы с JSON в SQL.
- `utility/` — Утилиты для очистки, кастинга и проверки статусов.

---
## Быстрая навигация
- **Портфолио**: [projects/portfolio/README.md](./projects/portfolio/README.md)
- **SaaS Аналитика**: [projects/telegram-analytics-saas/README.md](./projects/telegram-analytics-saas/README.md)
- **Инструкции по развертыванию**: [docs/telegram_bot_beget_guide.md](./docs/telegram_bot_beget_guide.md)
     
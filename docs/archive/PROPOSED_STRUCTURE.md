# 🏗️ Предложенная структура репозитория

## Принципы организации

1. **По типу проекта** - группируем похожие технологии вместе
2. **По статусу** - отделяем активные проекты от архивных
3. **Плоская иерархия** - максимум 3 уровня вложенности
4. **Единая документация** - один README на проект, остальное в `docs/`

---

## 📁 Новая структура

```
datascience-Roman/
│
├── 🤖 bots/                      # Все Telegram боты в одном месте
│   ├── telegram-analytics-saas/  # Активный: SaaS платформа (самый большой)
│   ├── invite-tracker/           # Активный: трекер приглашений
│   ├── member-tracker/           # Архив: старый трекер участников
│   └── mymeat-bot/              # Статус неизвестен
│
├── 🔄 automation/                # N8N и автоматизация
│   ├── superagent/              # Главный проект n8n
│   ├── daily-messages/          # Ежедневные отчеты
│   ├── weekly-reports/          # Еженедельные отчеты
│   └── workflows/               # Общие workflow конфигурации (было json_workflows)
│
├── 🤖 ai-agents/                 # AI агенты и ML проекты
│   ├── fishing-agent/           # Рыболовный AI агент
│   └── personal-agent/          # Другие персональные агенты
│
├── 💼 portfolio/                 # Портфолио и резюме
│   ├── projects/                # Описания проектов
│   ├── resume/                  # Резюме и cover letters
│   └── README.md
│
├── 🛠️ scripts/                  # Утилиты и скрипты
│   ├── automation/              # Автоматизация через Expect
│   ├── maintenance/             # Обслуживание и исправления
│   ├── reports/                 # Генерация отчетов
│   ├── tests/                   # Тесты
│   ├── setup/                   # Установка сервисов
│   └── utils/                   # Общие утилиты (deep_weave.py сюда)
│
├── 📊 data/                      # Данные и аналитика
│   ├── sql/                     # SQL запросы
│   └── js/                      # JavaScript для обработки данных
│
├── 📚 docs/                      # Централизованная документация
│   ├── deployment/              # Гайды по деплою
│   ├── api-references/          # API документация
│   └── guides/                  # Общие руководства
│
├── 🔧 config/                    # Конфигурационные файлы
│   ├── .cursor/                 # Cursor настройки и правила
│   └── templates/               # Шаблоны для проектов
│
└── 📦 archive/                   # Старые/неактивные проекты
    └── profit-premium/          # Неактивный проект
```

---

## 🔄 План миграции

### Этап 1: Группировка ботов
```bash
mkdir -p bots
mv projects/telegram-analytics-saas bots/
mv projects/invite_bot_new bots/invite-tracker
mv projects/telegram_member_tracker bots/member-tracker
mv projects/mymeat_bot bots/mymeat-bot
```

### Этап 2: Группировка N8N
```bash
mkdir -p automation
mv projects/superagent automation/
mv projects/n8n_daily_messages automation/daily-messages
mv projects/n8n_weekly_reports automation/weekly-reports
mv projects/json_workflows automation/workflows
```

### Этап 3: AI агенты
```bash
mkdir -p ai-agents
mv projects/personal_agent/fishing_ai_agent ai-agents/fishing-agent
rm -rf projects/personal_agent  # Если пустой
```

### Этап 4: Портфолио
```bash
# Портфолио остается, но реорганизуем внутри
mkdir -p portfolio/resume
mv portfolio/Resume_* portfolio/resume/
mv portfolio/Cover_Letter.md portfolio/resume/
```

### Этап 5: Скрипты
```bash
mkdir -p scripts/utils
mv deep_weave.py scripts/utils/
```

### Этап 6: Архив
```bash
mkdir -p archive
mv projects/profit-premium archive/
```

### Этап 7: Очистка
```bash
# Удаляем старые дубликаты
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name "beget_deployment/beget_deployment" -exec rm -rf {} +

# Удаляем пустую папку projects
rmdir projects 2>/dev/null || true
```

---

## ✅ Преимущества новой структуры

1. **Интуитивная навигация** - понятно где что лежит
2. **Группировка по технологиям** - все боты вместе, вся автоматизация вместе
3. **Меньше вложенности** - легче найти файл
4. **Четкое разделение** - активные проекты отдельно от архива
5. **Профессиональный вид** - структура как у enterprise проектов

---

## 📝 Следующие шаги

После реорганизации создадим:
1. **Агентов Cursor** для работы с каждой категорией
2. **Правила** для автоматизации задач
3. **Скилы** для специфичных операций

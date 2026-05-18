#!/bin/bash

# Скрипт реорганизации структуры репозитория datascience-Roman
# Версия: 1.0
# Дата: 2026-05-18

set -e  # Остановить при ошибке

REPO_ROOT="/Users/romanmuhachev/Documents/GitHub/datascience-Roman"

echo "🚀 Начинаем реорганизацию репозитория datascience-Roman"
echo "📁 Корень репозитория: $REPO_ROOT"
echo ""

# Функция для безопасного перемещения
safe_move() {
    local src=$1
    local dest=$2
    
    if [ -e "$src" ]; then
        echo "  ✓ Перемещение: $src -> $dest"
        mkdir -p "$(dirname "$dest")"
        mv "$src" "$dest"
    else
        echo "  ⚠ Пропуск (не найдено): $src"
    fi
}

# Переход в корень репозитория
cd "$REPO_ROOT"

echo "Шаг 1: Группировка Telegram ботов"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mkdir -p bots
safe_move "projects/telegram-analytics-saas" "bots/telegram-analytics-saas"
safe_move "projects/invite_bot_new" "bots/invite-tracker"
safe_move "projects/telegram_member_tracker" "bots/member-tracker"
safe_move "projects/mymeat_bot" "bots/mymeat-bot"
echo ""

echo "Шаг 2: Группировка N8N и автоматизации"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mkdir -p automation
safe_move "projects/superagent" "automation/superagent"
safe_move "projects/n8n_daily_messages" "automation/daily-messages"
safe_move "projects/n8n_weekly_reports" "automation/weekly-reports"
safe_move "projects/json_workflows" "automation/workflows"
echo ""

echo "Шаг 3: Группировка AI агентов"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mkdir -p ai-agents
safe_move "projects/personal_agent/fishing_ai_agent" "ai-agents/fishing-agent"
# Удалить пустую папку personal_agent если она пустая
if [ -d "projects/personal_agent" ] && [ -z "$(ls -A projects/personal_agent)" ]; then
    rmdir "projects/personal_agent"
    echo "  ✓ Удалена пустая папка: projects/personal_agent"
fi
echo ""

echo "Шаг 4: Портфолио (остается на месте, но реорганизуем внутри)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -d "projects/portfolio" ]; then
    mkdir -p projects/portfolio/resume
    find projects/portfolio -maxdepth 1 -name "Resume_*" -exec mv {} projects/portfolio/resume/ \; 2>/dev/null || true
    find projects/portfolio -maxdepth 1 -name "Cover_Letter*" -exec mv {} projects/portfolio/resume/ \; 2>/dev/null || true
    echo "  ✓ Реорганизовано: projects/portfolio"
fi
echo ""

echo "Шаг 5: Скрипты и утилиты"
echo "━━━━━━━━━━━━━━━━━━━━━━━━"
mkdir -p scripts/utils
safe_move "deep_weave.py" "scripts/utils/deep_weave.py"
echo ""

echo "Шаг 6: Архивирование неактивных проектов"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mkdir -p archive
safe_move "projects/profit-premium" "archive/profit-premium"
echo ""

echo "Шаг 7: Создание структуры для данных"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
mkdir -p data
# SQL уже есть, просто перемещаем
if [ -d "sql" ]; then
    safe_move "sql" "data/sql"
fi
# JS уже есть, просто перемещаем
if [ -d "js" ]; then
    safe_move "js" "data/js"
fi
echo ""

echo "Шаг 8: Очистка"
echo "━━━━━━━━━━━━━━━━━━"

# Удалить __pycache__
echo "  🧹 Удаление __pycache__ директорий..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Удалить дублирующиеся beget_deployment
echo "  🧹 Удаление дублирующихся beget_deployment..."
find bots -type d -path "*/beget_deployment/beget_deployment" -exec rm -rf {} + 2>/dev/null || true

# Удалить пустую папку projects если она пустая
if [ -d "projects" ] && [ -z "$(ls -A projects 2>/dev/null)" ]; then
    rmdir "projects"
    echo "  ✓ Удалена пустая папка: projects"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Реорганизация завершена успешно!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

echo "📊 Новая структура:"
echo ""
echo "datascience-Roman/"
echo "├── 🤖 bots/                  # Telegram боты"
echo "├── 🔄 automation/            # N8N и автоматизация"
echo "├── 🧠 ai-agents/             # AI проекты"
echo "├── 💼 projects/portfolio/    # Портфолио"
echo "├── 🛠️  scripts/              # Скрипты и утилиты"
echo "├── 📊 data/                  # SQL и JS для обработки данных"
echo "├── 📚 docs/                  # Документация"
echo "├── 📦 archive/               # Неактивные проекты"
echo "└── ⚙️  .cursor/              # Cursor агенты"
echo ""

echo "🎯 Следующие шаги:"
echo "1. Проверьте что все проекты на месте"
echo "2. Обновите пути в конфигах (если нужно)"
echo "3. Закоммитьте изменения:"
echo "   git add ."
echo "   git commit -m \"feat: Реорганизация структуры репозитория\""
echo ""
echo "💡 Используйте агентов Cursor для дальнейшей работы!"
echo "   Примеры: @backend, @frontend, @teamlead"
echo ""

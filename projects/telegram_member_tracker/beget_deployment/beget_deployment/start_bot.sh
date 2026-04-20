#!/bin/bash

# Скрипт запуска бота для Beget
# Использование: ./start_bot.sh

echo "🤖 Запуск Telegram Member Tracker Bot..."

# Проверяем наличие Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 не найден. Установите Python3."
    exit 1
fi

# Проверяем наличие файлов
if [ ! -f "invite_tracker.py" ]; then
    echo "❌ Файл invite_tracker.py не найден"
    exit 1
fi

if [ ! -f "credentials1.json" ]; then
    echo "❌ Файл credentials1.json не найден"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден"
    exit 1
fi

# Создаем директорию для логов
mkdir -p logs

# Запускаем бота в фоне
echo "🚀 Запуск бота..."
python3 invite_tracker.py > logs/bot_output.log 2>&1 &
BOT_PID=$!
echo $BOT_PID > bot.pid

echo "✅ Бот запущен! PID: $BOT_PID"
echo "📊 Логи: logs/bot_output.log"
echo "🛑 Остановить: kill $BOT_PID"

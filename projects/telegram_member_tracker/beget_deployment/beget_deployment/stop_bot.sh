#!/bin/bash

# Скрипт остановки бота
# Использование: ./stop_bot.sh

if [ -f "bot.pid" ]; then
    BOT_PID=$(cat bot.pid)
    if kill -0 $BOT_PID 2>/dev/null; then
        echo "🛑 Останавливаем бота (PID: $BOT_PID)..."
        kill $BOT_PID
        rm bot.pid
        echo "✅ Бот остановлен"
    else
        echo "⚠️ Бот не запущен или уже остановлен"
        rm bot.pid
    fi
else
    echo "⚠️ Файл bot.pid не найден. Бот возможно не запущен."
fi

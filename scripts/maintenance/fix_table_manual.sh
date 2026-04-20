#!/bin/bash

echo "🔧 Исправляем таблицу для Invite Tracker..."

# Переходим в директорию бота
cd /root/invite_bot

# Останавливаем текущий процесс
pkill -f invite_tracker.py
echo "✅ Процессы остановлены"

# Исправляем код - заменяем старую таблицу на новую
sed -i "s/SPREADSHEET_NAME = 'TelegramInviteTracking'/SPREADSHEET_NAME = '1_zWBxOJ-f_pY_uiwyZ-TWXKooul4K_waNXFWLaZ5f8I'/" invite_tracker.py

# Проверяем изменение
echo "📋 Текущие настройки:"
grep 'SPREADSHEET_NAME' invite_tracker.py

# Запускаем бота
echo "🚀 Запускаем Invite Tracker..."
source /root/bot_env/bin/activate
python invite_tracker.py > logs/bot_output.log 2>&1 &
BOT_PID=$!
echo $BOT_PID > bot.pid

echo "✅ Invite Tracker запущен с PID: $BOT_PID"
echo "📊 Записывает в таблицу: https://docs.google.com/spreadsheets/d/1_zWBxOJ-f_pY_uiwyZ-TWXKooul4K_waNXFWLaZ5f8I/edit"

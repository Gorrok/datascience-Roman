#!/bin/bash

# Скрипт исправления ботов на сервере
echo "🔧 Исправляем ботов..."

# Останавливаем все процессы
pkill -f invite_tracker.py
pkill -f bot.py
echo "✅ Процессы остановлены"

# Создаем invite-tracker.service
cat > /etc/systemd/system/invite-tracker.service << 'SERVICEEOF'
[Unit]
Description=Telegram Invite Tracker Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/invite_bot
ExecStart=/root/bot_env/bin/python /root/invite_bot/invite_tracker.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICEEOF
echo "✅ invite-tracker.service создан"

# Создаем member-tracker.service
cat > /etc/systemd/system/member-tracker.service << 'SERVICEEOF'
[Unit]
Description=Telegram Member Tracker Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/beget_deployment 2
ExecStart=/root/bot_env/bin/python /root/beget_deployment 2/bot.py
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICEEOF
echo "✅ member-tracker.service создан"

# Перезагружаем systemd
systemctl daemon-reload
echo "✅ systemd перезагружен"

# Включаем автозапуск
systemctl enable invite-tracker.service
systemctl enable member-tracker.service
echo "✅ Автозапуск включен"

# Запускаем сервисы
systemctl start invite-tracker.service
systemctl start member-tracker.service
echo "✅ Сервисы запущены"

# Ждем и проверяем
sleep 5

echo "=== СТАТУС INVITE TRACKER ==="
systemctl status invite-tracker.service --no-pager | head -10

echo "=== СТАТУС MEMBER TRACKER ==="
systemctl status member-tracker.service --no-pager | head -10

echo "=== ПРОЦЕССЫ PYTHON ==="
ps aux | grep python | grep -v grep

echo "🎉 Готово!"

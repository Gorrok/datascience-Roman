#!/bin/bash

# Простой скрипт исправления ботов
echo "🔧 Исправляем systemd сервисы..."

# Размаскируем invite-tracker
systemctl unmask invite-tracker.service

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

# Перезагружаем systemd
systemctl daemon-reload

# Включаем сервисы
systemctl enable invite-tracker.service
systemctl enable member-tracker.service

# Запускаем сервисы
systemctl start invite-tracker.service
systemctl start member-tracker.service

# Проверяем статус
echo "=== СТАТУС INVITE TRACKER ==="
systemctl status invite-tracker.service --no-pager | head -10

echo "=== СТАТУС MEMBER TRACKER ==="
systemctl status member-tracker.service --no-pager | head -10

# Проверяем процессы
echo "=== ПРОЦЕССЫ PYTHON ==="
ps aux | grep python | grep -v grep

echo "🎉 Готово!"

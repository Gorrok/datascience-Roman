#!/bin/bash

echo "🔧 Пересоздаем systemd сервисы..."

# Удаляем старые сервисы
systemctl stop invite-tracker.service 2>/dev/null
systemctl stop member-tracker.service 2>/dev/null
systemctl disable invite-tracker.service 2>/dev/null
systemctl disable member-tracker.service 2>/dev/null
rm -f /etc/systemd/system/invite-tracker.service
rm -f /etc/systemd/system/member-tracker.service

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
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
SERVICEEOF

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
RestartSec=5
StandardOutput=journal
StandardError=journal
Environment=PYTHONUNBUFFERED=1

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

echo "✅ Сервисы пересозданы"

#!/bin/bash

echo "🔧 Создаем systemd сервисы..."

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

# Создаем member-tracker.service
cat > /etc/systemd/system/member-tracker.service << 'SERVICEEOF'
[Unit]
Description=Telegram Member Tracker Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/beget_deployment 2
ExecStart=/root/bot_env/bin/python "/root/beget_deployment 2/bot.py"
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICEEOF

echo "✅ Сервисы созданы"

# Перезагружаем systemd
systemctl daemon-reload
echo "✅ SystemD перезагружен"

# Включаем автозапуск
systemctl enable invite-tracker.service
systemctl enable member-tracker.service
echo "✅ Автозапуск включен"

# Запускаем сервисы
systemctl start invite-tracker.service
systemctl start member-tracker.service
echo "✅ Сервисы запущены"

# Проверяем статус
echo "=== СТАТУС INVITE TRACKER ==="
systemctl status invite-tracker.service --no-pager

echo "=== СТАТУС MEMBER TRACKER ==="
systemctl status member-tracker.service --no-pager

echo "=== ПРОЦЕССЫ PYTHON ==="
ps aux | grep python | grep -v unattended | grep -v fail2ban | grep -v grep

echo "🎉 Готово!"

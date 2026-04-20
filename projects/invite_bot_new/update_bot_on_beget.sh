#!/bin/bash
# Быстрое обновление бота на Beget

# Цвета
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}=== Обновление бота на Beget ===${NC}"
echo ""

# Проверка наличия invite_tracker.py
if [ ! -f "invite_tracker.py" ]; then
    echo "Ошибка: invite_tracker.py не найден в текущей директории"
    exit 1
fi

echo -e "${YELLOW}Введите данные для подключения к Beget:${NC}"
read -p "Логин: " BEGET_USER
read -p "Хост (например, yourname.beget.tech): " BEGET_HOST
read -s -p "Пароль: " BEGET_PASS
echo ""

echo -e "${YELLOW}Подключение к серверу...${NC}"

# Создаём временный expect скрипт
cat > /tmp/update_bot.exp << 'EOF'
#!/usr/bin/expect -f
set beget_user [lindex $argv 0]
set beget_host [lindex $argv 1]
set beget_pass [lindex $argv 2]
set timeout 30

spawn ssh $beget_user@$beget_host

expect {
    "password:" {
        send "$beget_pass\r"
    }
    "yes/no" {
        send "yes\r"
        exp_continue
    }
}

expect "$ "
send "cd ../home/telegram-bot/bot2\r"

expect "$ "
send "pkill -f invite_tracker.py\r"

expect "$ "
send "sleep 2\r"

expect "$ "
send "ps aux | grep invite_tracker\r"

expect "$ "
send "source venv/bin/activate\r"

expect "$ "
send "nohup python3 invite_tracker.py > logs/bot_output.log 2>&1 &\r"

expect "$ "
send "echo \$! > bot.pid\r"

expect "$ "
send "sleep 2\r"

expect "$ "
send "cat bot.pid\r"

expect "$ "
send "tail -20 logs/bot_output.log\r"

expect "$ "
send "exit\r"

expect eof
EOF

chmod +x /tmp/update_bot.exp

# Загружаем обновлённый файл на сервер
echo -e "${YELLOW}Загрузка обновлённого файла...${NC}"
sshpass -p "$BEGET_PASS" scp invite_tracker.py $BEGET_USER@$BEGET_HOST:../home/telegram-bot/bot2/

# Запускаем скрипт обновления
/tmp/update_bot.exp "$BEGET_USER" "$BEGET_HOST" "$BEGET_PASS"

# Удаляем временный файл
rm /tmp/update_bot.exp

echo ""
echo -e "${GREEN}✓ Готово!${NC}"

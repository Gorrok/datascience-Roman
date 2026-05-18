#!/bin/bash
# Скрипт для создания готового к деплою архива

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Создание архива для деплоя на Beget ===${NC}"

# Имя архива
ARCHIVE_NAME="mickey_invite_bot_$(date +%Y%m%d_%H%M%S).tar.gz"

# Файлы для включения в архив
FILES=(
    "invite_tracker.py"
    "requirements.txt"
    "invitebot.service"
    "start_bot.sh"
    "stop_bot.sh"
    "check_status.sh"
)

# Проверка наличия файлов
echo -e "${YELLOW}Проверка файлов...${NC}"
MISSING_FILES=0
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "  ✗ $file - не найден"
        MISSING_FILES=$((MISSING_FILES + 1))
    else
        echo -e "  ✓ $file"
    fi
done

if [ $MISSING_FILES -gt 0 ]; then
    echo -e "${YELLOW}Внимание: Некоторые файлы не найдены${NC}"
fi

# Создание архива
echo -e "${YELLOW}Создание архива...${NC}"
tar -czf "$ARCHIVE_NAME" "${FILES[@]}" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Архив создан: $ARCHIVE_NAME${NC}"
    
    # Размер архива
    SIZE=$(du -h "$ARCHIVE_NAME" | cut -f1)
    echo -e "${GREEN}  Размер: $SIZE${NC}"
    
    echo ""
    echo -e "${YELLOW}=== НАСТРОЙКИ MICKEY КАНАЛА ===${NC}"
    echo "Токен:  7773528819:AAFT2HUPl-axcFCvYVYc5uHmgQZfMNKcOfE"
    echo "Канал:  -1001589094262"
    echo "Sheets: Invite tracker mickey"
    echo ""
    echo -e "${YELLOW}=== Следующие шаги ===${NC}"
    echo "1. Загрузите архив на Beget через SCP или FileZilla"
    echo "2. Подключитесь: ssh user@host.beget.tech"
    echo "3. Распакуйте: tar -xzf $ARCHIVE_NAME"
    echo "4. НЕ ЗАБУДЬТЕ загрузить credentials.json!"
    echo "5. Создайте venv: python3 -m venv venv"
    echo "6. Активируйте: source venv/bin/activate"
    echo "7. Установите: pip install -r requirements.txt"
    echo "8. Настройте пути в invitebot.service"
    echo "9. Установите сервис: sudo cp invitebot.service /etc/systemd/system/"
    echo "10. Запустите: sudo systemctl start invitebot.service"
else
    echo -e "${RED}✗ Ошибка создания архива${NC}"
    exit 1
fi

#!/bin/bash
# Скрипт остановки бота на Beget

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Остановка Invite Bot ===${NC}"

# Проверка наличия PID файла
if [ ! -f "bot.pid" ]; then
    echo -e "${RED}Файл bot.pid не найден. Бот не запущен?${NC}"
    
    # Поиск процесса по имени
    echo -e "${YELLOW}Поиск процесса invite_bot.py...${NC}"
    PIDS=$(pgrep -f "invite_bot.py")
    
    if [ -z "$PIDS" ]; then
        echo -e "${GREEN}Процессы не найдены${NC}"
        exit 0
    else
        echo -e "${YELLOW}Найдены процессы: $PIDS${NC}"
        echo -e "${YELLOW}Остановка процессов...${NC}"
        kill $PIDS
        sleep 2
        
        # Проверка, завершились ли процессы
        REMAINING=$(pgrep -f "invite_bot.py")
        if [ -z "$REMAINING" ]; then
            echo -e "${GREEN}✓ Все процессы остановлены${NC}"
        else
            echo -e "${YELLOW}Принудительная остановка...${NC}"
            kill -9 $REMAINING
            echo -e "${GREEN}✓ Процессы принудительно остановлены${NC}"
        fi
        exit 0
    fi
fi

# Чтение PID из файла
PID=$(cat bot.pid)

# Проверка, запущен ли процесс
if ! ps -p $PID > /dev/null 2>&1; then
    echo -e "${YELLOW}Процесс с PID $PID не найден${NC}"
    rm bot.pid
    exit 0
fi

# Остановка процесса
echo -e "${YELLOW}Остановка бота (PID: $PID)...${NC}"
kill $PID

# Ожидание завершения
sleep 2

# Проверка завершения
if ps -p $PID > /dev/null 2>&1; then
    echo -e "${YELLOW}Процесс не завершился, принудительная остановка...${NC}"
    kill -9 $PID
    sleep 1
fi

# Финальная проверка
if ps -p $PID > /dev/null 2>&1; then
    echo -e "${RED}✗ Не удалось остановить бота${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Бот успешно остановлен${NC}"
    rm bot.pid
fi

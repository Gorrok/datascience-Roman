#!/bin/bash
# Скрипт проверки статуса бота

# Цвета для вывода
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Статус Invite Bot ===${NC}"
echo ""

# Проверка PID файла
if [ -f "bot.pid" ]; then
    PID=$(cat bot.pid)
    echo -e "${YELLOW}PID файл найден: $PID${NC}"
    
    if ps -p $PID > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Бот запущен и работает (PID: $PID)${NC}"
        
        # Информация о процессе
        echo ""
        echo -e "${BLUE}Информация о процессе:${NC}"
        ps -p $PID -o pid,ppid,cmd,%mem,%cpu,etime
        
        # Размер лог-файла
        if [ -f "logs/bot_output.log" ]; then
            LOG_SIZE=$(du -h logs/bot_output.log | cut -f1)
            echo ""
            echo -e "${BLUE}Размер лога: ${NC}$LOG_SIZE"
            
            # Последние 10 строк лога
            echo ""
            echo -e "${BLUE}Последние 10 строк лога:${NC}"
            tail -n 10 logs/bot_output.log
        fi
    else
        echo -e "${RED}✗ Процесс с PID $PID не запущен${NC}"
        echo -e "${YELLOW}Используйте ./start_bot.sh для запуска${NC}"
    fi
else
    echo -e "${YELLOW}PID файл не найден${NC}"
    
    # Поиск процесса по имени
    PIDS=$(pgrep -f "invite_bot.py")
    if [ -z "$PIDS" ]; then
        echo -e "${RED}✗ Бот не запущен${NC}"
        echo -e "${YELLOW}Используйте ./start_bot.sh для запуска${NC}"
    else
        echo -e "${YELLOW}Найдены процессы invite_bot.py:${NC}"
        ps -p $PIDS -o pid,ppid,cmd,%mem,%cpu,etime
        echo ""
        echo -e "${YELLOW}Создайте bot.pid вручную или перезапустите бота${NC}"
    fi
fi

# Проверка виртуального окружения
echo ""
echo -e "${BLUE}Виртуальное окружение:${NC}"
if [ -d "venv" ]; then
    echo -e "${GREEN}✓ venv найдено${NC}"
else
    echo -e "${RED}✗ venv не найдено${NC}"
fi

# Проверка конфигурации
echo ""
echo -e "${BLUE}Конфигурация:${NC}"
if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env найден${NC}"
else
    echo -e "${RED}✗ .env не найден${NC}"
fi

if [ -f "credentials.json" ]; then
    echo -e "${GREEN}✓ credentials.json найден${NC}"
else
    echo -e "${RED}✗ credentials.json не найден${NC}"
fi

# Проверка логов
echo ""
echo -e "${BLUE}Логи:${NC}"
if [ -d "logs" ]; then
    LOG_COUNT=$(ls logs/*.log 2>/dev/null | wc -l)
    echo -e "${GREEN}✓ Директория logs найдена (файлов: $LOG_COUNT)${NC}"
    
    if [ -f "logs/bot.log" ]; then
        ERROR_COUNT=$(grep -c "ERROR" logs/bot.log 2>/dev/null || echo "0")
        echo -e "${YELLOW}  Ошибок в логе: $ERROR_COUNT${NC}"
    fi
else
    echo -e "${YELLOW}Директория logs не найдена${NC}"
fi

echo ""

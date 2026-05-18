#!/bin/bash
# Скрипт деплоя Job Vacancy Agent на Ubuntu сервер

set -e  # Остановить при ошибке

echo "🚀 Деплой Job Vacancy Agent на Ubuntu"
echo "======================================"

# Цвета для вывода
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Проверка что запущено на Ubuntu
if [ ! -f /etc/os-release ]; then
    echo "❌ Это не Linux система!"
    exit 1
fi

# 1. Обновление системы
echo -e "\n${YELLOW}1. Обновление системы...${NC}"
sudo apt update
sudo apt upgrade -y

# 2. Установка Python 3.11+
echo -e "\n${YELLOW}2. Установка Python...${NC}"
if ! command -v python3.11 &> /dev/null; then
    sudo apt install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install -y python3.11 python3.11-venv python3.11-dev
    echo -e "${GREEN}✓ Python 3.11 установлен${NC}"
else
    echo -e "${GREEN}✓ Python 3.11 уже установлен${NC}"
fi

# 3. Установка Ollama
echo -e "\n${YELLOW}3. Установка Ollama...${NC}"
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
    echo -e "${GREEN}✓ Ollama установлен${NC}"
else
    echo -e "${GREEN}✓ Ollama уже установлен${NC}"
fi

# Проверка что Ollama запущен
if ! systemctl is-active --quiet ollama; then
    sudo systemctl start ollama
    echo -e "${GREEN}✓ Ollama запущен${NC}"
fi

# 4. Скачивание модели Hermes
echo -e "\n${YELLOW}4. Скачивание модели Hermes AI...${NC}"
if ! ollama list | grep -q hermes3; then
    echo "Скачивание hermes3:8b (это может занять несколько минут)..."
    ollama pull hermes3:8b
    echo -e "${GREEN}✓ Модель hermes3:8b скачана${NC}"
else
    echo -e "${GREEN}✓ Модель hermes3:8b уже скачана${NC}"
fi

# 5. Создание виртуального окружения
echo -e "\n${YELLOW}5. Создание виртуального окружения...${NC}"
if [ ! -d "venv" ]; then
    python3.11 -m venv venv
    echo -e "${GREEN}✓ Виртуальное окружение создано${NC}"
else
    echo -e "${GREEN}✓ Виртуальное окружение уже существует${NC}"
fi

# Активация venv
source venv/bin/activate

# 6. Установка зависимостей
echo -e "\n${YELLOW}6. Установка Python зависимостей...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Зависимости установлены${NC}"

# 7. Проверка secrets.py
echo -e "\n${YELLOW}7. Проверка конфигурации...${NC}"
if [ ! -f "secrets.py" ]; then
    echo -e "${YELLOW}⚠️  Файл secrets.py не найден!${NC}"
    echo "Создаю из примера..."
    cp secrets.py.example secrets.py
    echo -e "${YELLOW}📝 ВАЖНО: Отредактируйте secrets.py и заполните свои ключи!${NC}"
    echo "   nano secrets.py"
    exit 0
else
    echo -e "${GREEN}✓ Файл secrets.py существует${NC}"
fi

# 8. Тестовый запуск
echo -e "\n${YELLOW}8. Тестовая проверка системы...${NC}"
python main.py --test

if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✅ Все проверки пройдены!${NC}"
else
    echo -e "\n${YELLOW}⚠️  Есть ошибки в конфигурации${NC}"
    echo "Проверьте secrets.py и повторите попытку"
    exit 1
fi

# 9. Установка systemd service
echo -e "\n${YELLOW}9. Установка systemd сервиса...${NC}"

# Получаем текущую директорию и пользователя
CURRENT_DIR=$(pwd)
CURRENT_USER=$(whoami)

# Создаем service файл
cat > /tmp/vacancy-agent.service <<EOF
[Unit]
Description=Job Vacancy Agent
After=network.target ollama.service

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
Environment="PATH=$CURRENT_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$CURRENT_DIR/venv/bin/python $CURRENT_DIR/main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Копируем в systemd
sudo cp /tmp/vacancy-agent.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vacancy-agent
echo -e "${GREEN}✓ Systemd сервис установлен${NC}"

# 10. Запуск сервиса
echo -e "\n${YELLOW}10. Запуск сервиса...${NC}"
sudo systemctl start vacancy-agent

sleep 2

if systemctl is-active --quiet vacancy-agent; then
    echo -e "${GREEN}✓ Сервис успешно запущен!${NC}"
else
    echo -e "${YELLOW}⚠️  Сервис не запущен, проверьте логи:${NC}"
    echo "   sudo journalctl -u vacancy-agent -f"
    exit 1
fi

# Финал
echo -e "\n${GREEN}======================================"
echo "✅ Деплой завершен успешно!"
echo "======================================${NC}"
echo ""
echo "📊 Статус сервиса:"
echo "   sudo systemctl status vacancy-agent"
echo ""
echo "📋 Логи:"
echo "   sudo journalctl -u vacancy-agent -f"
echo "   tail -f vacancy_agent.log"
echo ""
echo "🛑 Остановка:"
echo "   sudo systemctl stop vacancy-agent"
echo ""
echo "🔄 Перезапуск:"
echo "   sudo systemctl restart vacancy-agent"
echo ""
echo "🗑️  Удаление сервиса:"
echo "   sudo systemctl stop vacancy-agent"
echo "   sudo systemctl disable vacancy-agent"
echo "   sudo rm /etc/systemd/system/vacancy-agent.service"
echo ""

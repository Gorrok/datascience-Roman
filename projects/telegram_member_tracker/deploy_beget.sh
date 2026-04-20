#!/bin/bash

# Скрипт для развертывания бота на Beget хостинге
# Использование: ./deploy_beget.sh

echo "🚀 Начинаем развертывание Telegram Member Tracker Bot на Beget"

# Проверяем, что мы в правильной директории
if [ ! -f "bot.py" ]; then
    echo "❌ Ошибка: файл bot.py не найден. Перейдите в директорию с ботом."
    exit 1
fi

echo "📁 Текущая директория: $(pwd)"

# Создаем виртуальное окружение
echo "🐍 Создаем виртуальное окружение..."
python3 -m venv bot_env

# Активируем виртуальное окружение
echo "🔄 Активируем виртуальное окружение..."
source bot_env/bin/activate

# Обновляем pip
echo "⬆️ Обновляем pip..."
pip install --upgrade pip

# Устанавливаем зависимости
echo "📦 Устанавливаем зависимости..."
pip install -r requirements.txt

# Проверяем наличие credentials.json
if [ ! -f "credentials.json" ]; then
    echo "⚠️  ВНИМАНИЕ: файл credentials.json не найден!"
    echo "   Следуйте инструкциям в google_sheets_setup.md для настройки Google Sheets API"
    echo "   Без этого файла бот не сможет сохранять данные"
fi

# Проверяем конфигурацию
echo "🔍 Проверяем конфигурацию..."
python test_bot.py

if [ $? -eq 0 ]; then
    echo "✅ Все проверки пройдены!"

    # Создаем скрипт запуска
    echo "📝 Создаем скрипт запуска..."
    cat > start_bot.sh << 'EOF'
#!/bin/bash
# Скрипт для запуска бота

# Переходим в директорию бота
cd "$(dirname "$0")"

# Активируем виртуальное окружение
source bot_env/bin/activate

# Запускаем бота в фоне
echo "🤖 Запускаем бота..."
nohup python bot.py > logs/bot_output.log 2>&1 &
echo $! > bot.pid
echo "✅ Бот запущен! PID: $(cat bot.pid)"
EOF

    chmod +x start_bot.sh

    # Создаем скрипт остановки
    cat > stop_bot.sh << 'EOF'
#!/bin/bash
# Скрипт для остановки бота

if [ -f "bot.pid" ]; then
    PID=$(cat bot.pid)
    if kill -0 $PID 2>/dev/null; then
        echo "🛑 Останавливаем бота (PID: $PID)..."
        kill $PID
        rm bot.pid
        echo "✅ Бот остановлен"
    else
        echo "⚠️ Бот не запущен или уже остановлен"
        rm bot.pid
    fi
else
    echo "⚠️ Файл bot.pid не найден. Бот возможно не запущен."
fi
EOF

    chmod +x stop_bot.sh

    # Создаем скрипт перезапуска
    cat > restart_bot.sh << 'EOF'
#!/bin/bash
# Скрипт для перезапуска бота

echo "🔄 Перезапускаем бота..."
./stop_bot.sh
sleep 2
./start_bot.sh
EOF

    chmod +x restart_bot.sh

    echo ""
    echo "🎉 Развертывание завершено!"
    echo ""
    echo "📋 Доступные команды:"
    echo "  ./start_bot.sh    - запустить бота"
    echo "  ./stop_bot.sh     - остановить бота"
    echo "  ./restart_bot.sh  - перезапустить бота"
    echo ""
    echo "📊 Мониторинг:"
    echo "  tail -f logs/bot.log           - просмотр логов"
    echo "  ps aux | grep python          - проверка процесса"
    echo "  python test_bot.py            - проверка конфигурации"
    echo ""
    echo "🚀 Для запуска бота выполните:"
    echo "  ./start_bot.sh"

else
    echo "❌ Некоторые проверки провалены. Исправьте ошибки и повторите развертывание."
    exit 1
fi

#!/bin/bash

# Data Science Project Backup Script
# Автоматический бэкап проекта в Git

set -e  # Остановить выполнение при ошибке

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функция для вывода сообщений
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✓${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

# Проверка наличия Git
if ! command -v git &> /dev/null; then
    error "Git не установлен. Установите Git для использования бэкапов."
    exit 1
fi

# Проверка инициализации Git репозитория
if [ ! -d ".git" ]; then
    log "Инициализация Git репозитория..."
    git init
    success "Git репозиторий инициализирован"
fi

# Добавление remote origin если его нет
if ! git remote get-url origin &> /dev/null; then
    log "Добавление remote origin..."
    git remote add origin https://github.com/Gorrok/datascience-Roman.git
    success "Remote origin добавлен"
fi

# Получение текущей ветки
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

# Проверка статуса репозитория
log "Проверка статуса репозитория..."
git status --porcelain

# Добавление всех изменений
log "Добавление изменений..."
git add .

# Проверка есть ли изменения для коммита
if git diff --staged --quiet; then
    warning "Нет изменений для коммита"
    exit 0
fi

# Создание коммита
COMMIT_MESSAGE="Backup: $(date +'%Y-%m-%d %H:%M:%S')"
log "Создание коммита: $COMMIT_MESSAGE"
git commit -m "$COMMIT_MESSAGE"
success "Коммит создан"

# Отправка в удаленный репозиторий
log "Отправка изменений в GitHub..."
if git push origin "$CURRENT_BRANCH"; then
    success "Бэкап успешно отправлен в GitHub"
else
    warning "Не удалось отправить в GitHub. Возможно, нужно настроить аутентификацию."
    log "Для настройки аутентификации используйте:"
    echo "  git config --global user.name 'Your Name'"
    echo "  git config --global user.email 'your.email@example.com'"
    echo "  Для GitHub используйте Personal Access Token вместо пароля"
fi

log "Бэкап завершен!"

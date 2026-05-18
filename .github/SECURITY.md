# 🔒 Политика безопасности

## Защита секретов

Этот репозиторий настроен для автоматической защиты от утечки секретов.

### 🛡️ Установленная защита:

#### 1. Git Hooks
- **Pre-commit hook** - проверяет перед каждым коммитом
- **Pre-push hook** - финальная проверка перед push

#### 2. Cursor Rules
- **security.mdc** - правила для AI-ассистента

#### 3. .gitignore
Автоматически исключает:
- `secrets.py`
- `*.session` (Telegram сессии)
- `.env`, `.env.local`, `.env.production`
- `credentials.json`

### 📋 Запрещено коммитить:

❌ **Файлы:**
- `secrets.py` (только `.example` версии!)
- `*.session`, `*.session-journal`
- `.env`, `.env.local`, `.env.production`
- `credentials.json`, `service-account.json`
- `*.pem`, `*.key`
- Любые файлы с реальными ключами

❌ **Строки:**
- API ключи
- Токены доступа
- Пароли
- Хэши
- Приватные ключи

### ✅ Как правильно хранить секреты:

#### Способ 1: secrets.py.example
```python
# secrets.py.example (в git) ✅
API_KEY = "your_api_key_here"
TOKEN = "your_token_here"

# secrets.py (НЕ в git) ✅
API_KEY = "AIzaSyBoLtzWJNGJ..."  # реальный ключ
TOKEN = "ghp_abc123..."
```

#### Способ 2: .env файлы
```bash
# .env.example (в git) ✅
API_KEY=your_api_key_here
TOKEN=your_token_here

# .env (НЕ в git) ✅
API_KEY=AIzaSyBoLtzWJNGJ...
TOKEN=ghp_abc123...
```

#### Способ 3: Переменные окружения
```python
import os
API_KEY = os.getenv("API_KEY")
```

### 🚀 Настройка для новых разработчиков:

```bash
# 1. Клонировать репозиторий
git clone https://github.com/Gorrok/datascience-Roman.git

# 2. Hooks уже настроены автоматически в .git/hooks/

# 3. Создать локальные secrets файлы
cp ai-agents/fishing-agent/secrets.py.example ai-agents/fishing-agent/secrets.py
cp ai-agents/job-vacancy-agent/secrets.py.example ai-agents/job-vacancy-agent/secrets.py

# 4. Заполнить своими ключами
nano ai-agents/fishing-agent/secrets.py
```

### 🔍 Проверка перед коммитом:

```bash
# 1. Проверить что будет закоммичено
git status
git diff --staged

# 2. Поиск возможных секретов
git diff --staged | grep -iE "api_key|secret|password|token"

# 3. Коммит (hook проверит автоматически)
git commit -m "..."
```

### ⚠️ Если случайно закоммитили секрет:

#### До push:
```bash
# Отменить последний коммит
git reset HEAD~1

# Удалить файл из staging
git reset HEAD secrets.py

# Закоммитить без секретов
git add <безопасные файлы>
git commit -m "..."
```

#### После push:
```bash
# 1. НЕМЕДЛЕННО отзовите все ключи!
# 2. Очистите историю
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/secrets.py' \
  --prune-empty --tag-name-filter cat -- --all

# 3. Force push
git push --force --all
```

### 🆘 Что делать если hook блокирует:

#### Ложное срабатывание:
```bash
# Пропустить проверку (используйте осторожно!)
git commit --no-verify
git push --no-verify
```

#### Реальная проблема:
1. Удалите секретные файлы из staging
2. Используйте `.example` файлы
3. Добавьте в `.gitignore`

### 🔐 Лучшие практики:

1. ✅ **Всегда** используйте `.example` файлы
2. ✅ **Никогда** не коммитьте реальные ключи
3. ✅ **Проверяйте** `git diff` перед коммитом
4. ✅ **Используйте** переменные окружения
5. ✅ **Храните** секреты в password manager
6. ✅ **Ротируйте** ключи регулярно

### 📞 Сообщить о проблеме:

Если вы обнаружили утечку секретов в репозитории:
1. НЕ создавайте публичный issue
2. Напишите напрямую владельцу репозитория
3. Укажите коммит и файл с утечкой

---

## 🔒 Помните: Безопасность - это не опция, это необходимость!

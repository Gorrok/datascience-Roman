# 🚀 Деплой Couples Planner как полноценное приложение

Эта инструкция покажет как задеплоить ваше приложение чтобы оно выглядело и работало как Telegram Wallet - полноценное, быстрое и красивое.

## 🎯 Что мы получим в итоге:

- ✅ Приложение открывается на весь экран в Telegram
- ✅ Плавные анимации и переходы
- ✅ Работает как нативное приложение
- ✅ Быстрая загрузка
- ✅ Красивый дизайн с градиентами
- ✅ Доступно 24/7 из любой точки мира

---

## 📱 Шаг 1: Подготовка Mini App для production

### 1.1 Обновите конфигурацию Vite

Создайте файл `mini-app/vite.config.js`:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
      }
    }
  },
  server: {
    port: 5173,
    host: true
  }
})
```

### 1.2 Создайте production .env

```bash
cd mini-app
cp .env.example .env.production

# Отредактируйте .env.production
VITE_API_URL=https://your-backend-domain.com/api
```

---

## ☁️ Шаг 2: Деплой Backend + Bot (Railway - БЕСПЛАТНО)

[Railway](https://railway.app) предоставляет бесплатно 500 часов в месяц - идеально для личного проекта!

### 2.1 Подготовка проекта

```bash
cd backend

# Создайте requirements.txt для production
cat > requirements-prod.txt << 'EOF'
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlalchemy==2.0.25
pydantic==2.5.3
python-dotenv==1.0.0
aiosqlite==0.19.0
python-multipart==0.0.6
EOF
```

### 2.2 Создайте Procfile

```bash
# В корне backend/
cat > Procfile << 'EOF'
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
EOF
```

### 2.3 Деплой на Railway

1. Зарегистрируйтесь на [Railway.app](https://railway.app)
2. Нажмите "New Project" → "Deploy from GitHub repo"
3. Выберите ваш репозиторий
4. Railway автоматически определит Python проект
5. Настройте переменные окружения:
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен
   USER_1_ID=ваш_id
   USER_1_NAME=Роман
   USER_2_ID=катя_id
   USER_2_NAME=Катя
   DATABASE_URL=sqlite+aiosqlite:///./couples_planner.db
   ```

6. Railway даст вам URL типа: `https://your-project.up.railway.app`

### 2.4 Деплой Bot отдельно

На Railway создайте еще один сервис для бота:

1. "New Service" → "GitHub Repo" → выберите тот же репозиторий
2. Укажите папку `bot` как root directory
3. Добавьте те же переменные окружения
4. Добавьте:
   ```
   API_HOST=https://your-backend.up.railway.app
   API_PORT=443
   ```

5. Создайте `bot/Procfile`:
   ```
   worker: python bot.py
   ```

---

## 🌐 Шаг 3: Деплой Mini App (Vercel - БЕСПЛАТНО)

[Vercel](https://vercel.com) идеально подходит для React приложений.

### 3.1 Подготовка

```bash
cd mini-app

# Создайте vercel.json
cat > vercel.json << 'EOF'
{
  "buildCommand": "npm run build",
  "outputDirectory": "dist",
  "framework": "vite",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
EOF
```

### 3.2 Деплой

1. Зарегистрируйтесь на [Vercel.com](https://vercel.com)
2. Нажмите "Add New Project"
3. Import вашего GitHub репозитория
4. Настройки:
   - **Root Directory**: `mini-app`
   - **Framework Preset**: Vite
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

5. Environment Variables:
   ```
   VITE_API_URL=https://your-backend.up.railway.app/api
   ```

6. Нажмите "Deploy"

Vercel даст вам URL типа: `https://your-app.vercel.app`

---

## 🤖 Шаг 4: Настройка Mini App в BotFather

Это КРИТИЧЕСКИ ВАЖНЫЙ шаг для работы как полноценное приложение!

### 4.1 Создайте Mini App

1. Откройте [@BotFather](https://t.me/BotFather)
2. Отправьте `/newapp`
3. Выберите вашего бота
4. Заполните:
   - **Title**: Наш планировщик 💕
   - **Description**: Планируем совместные дела и хотелки
   - **Photo**: Загрузите иконку 640x360 px (можете создать на [Canva](https://canva.com))
   - **Demo GIF/Video**: (опционально)
   - **Web App URL**: `https://your-app.vercel.app`
   - **Short name**: `couples_planner` (будет в URL)

5. BotFather даст вам ссылку типа: `https://t.me/your_bot/couples_planner`

### 4.2 Настройте кнопку меню

```
/setmenubutton
→ Выберите вашего бота
→ Text: 💕 Открыть планировщик
→ URL: https://t.me/your_bot/couples_planner
```

---

## 🎨 Шаг 5: Финальные штрихи для нативного вида

### 5.1 Обновите meta-теги (mini-app/index.html)

```html
<!DOCTYPE html>
<html lang="ru">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover" />
    <meta name="theme-color" content="#ff6b9d" />
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <title>Наш планировщик 💕</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
      /* Убираем мерцание при загрузке */
      body {
        margin: 0;
        background: linear-gradient(180deg, #ffeef8 0%, #fff5f7 50%, #ffffff 100%);
      }
    </style>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>
```

### 5.2 Обновите App.jsx для полноэкранного режима

В начале компонента добавьте:

```javascript
useEffect(() => {
  tg.ready();
  tg.expand(); // Разворачиваем на весь экран
  tg.enableClosingConfirmation(); // Подтверждение при закрытии
  
  // Убираем кнопку "Назад"
  tg.BackButton.hide();
  
  // Настраиваем цвет хедера
  tg.setHeaderColor('#ff6b9d');
  tg.setBackgroundColor('#ffeef8');
  
  loadPlans();
}, []);
```

---

## 🔒 Шаг 6: Безопасность (ВАЖНО!)

### 6.1 Добавьте проверку Telegram данных в Backend

Создайте `backend/app/core/security.py`:

```python
import hmac
import hashlib
from urllib.parse import parse_qs

def validate_telegram_webapp_data(init_data: str, bot_token: str) -> bool:
    """
    Проверяет подлинность данных от Telegram Mini App
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-mini-app
    """
    try:
        parsed_data = parse_qs(init_data)
        hash_str = parsed_data.get('hash', [''])[0]
        
        # Убираем hash из данных
        data_check_arr = []
        for key, value in parsed_data.items():
            if key != 'hash':
                data_check_arr.append(f"{key}={value[0]}")
        
        data_check_arr.sort()
        data_check_string = '\n'.join(data_check_arr)
        
        # Создаем secret key
        secret_key = hmac.new(
            "WebAppData".encode(),
            bot_token.encode(),
            hashlib.sha256
        ).digest()
        
        # Проверяем hash
        calculated_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return calculated_hash == hash_str
    except Exception:
        return False
```

### 6.2 Добавьте middleware для проверки

```python
from fastapi import Header, HTTPException

async def verify_telegram_webapp(
    x_telegram_init_data: str = Header(None)
):
    if not x_telegram_init_data:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not validate_telegram_webapp_data(x_telegram_init_data, settings.TELEGRAM_BOT_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid Telegram data")
```

---

## ✅ Шаг 7: Проверка

1. **Откройте вашего бота в Telegram**
2. **Отправьте** `/start`
3. **Нажмите** кнопку меню или "🎯 Открыть планировщик"
4. **Приложение должно:**
   - Открыться на весь экран
   - Показать красивый градиентный хедер
   - Работать плавно с анимациями
   - Загружаться быстро

---

## 🎯 Что получилось:

✅ **Полноценное приложение** - открывается как Wallet, работает нативно  
✅ **Красивый дизайн** - градиенты, анимации, милые детали  
✅ **Быстрая работа** - все задеплоено на быстрых серверах  
✅ **Бесплатно** - Railway + Vercel = $0/месяц  
✅ **Доступно 24/7** - работает из любой точки мира  
✅ **Безопасно** - только вы двое имеете доступ  

---

## 💰 Стоимость:

| Сервис | План | Стоимость |
|--------|------|-----------|
| Railway | Hobby | **Бесплатно** (500 часов/месяц) |
| Vercel | Hobby | **Бесплатно** (неограниченно) |
| **ИТОГО** | | **$0/месяц** 🎉 |

---

## 📱 Альтернатива: Полностью бесплатный деплой на Render

Если Railway закончится:

1. **Backend**: [Render.com](https://render.com) - 750 часов бесплатно
2. **Bot**: Render.com Web Service
3. **Mini App**: [Netlify](https://netlify.com) - бесплатно

---

## 🆘 Troubleshooting

### Mini App не открывается
- Проверьте что URL в BotFather правильный
- Убедитесь что Vercel задеплоил успешно
- Проверьте консоль браузера (Telegram Desktop → DevTools)

### Не работают уведомления
- Проверьте что бот задеплоен на Railway
- Проверьте переменные окружения (BOT_TOKEN)
- Посмотрите логи на Railway

### Медленная загрузка
- Включите минификацию в vite.config.js
- Уберите console.log из production
- Используйте Vercel Pro (но это платно)

---

## 🎨 Дополнительные улучшения

### Иконка приложения

Создайте иконку 512x512 px на [Canva](https://canva.com):
- Фон: градиент #ff6b9d → #c86dd7
- Эмодзи: 💕 или 🎯
- Экспортируйте как PNG

### Сплэш скрин

Добавьте красивую загрузку:

```css
/* В App.css */
.loading {
  background: linear-gradient(135deg, #ff6b9d, #c86dd7);
  color: white;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
```

---

**Готово! Теперь у вас полноценное приложение как Telegram Wallet, только для планирования ваших совместных дел! 💕**

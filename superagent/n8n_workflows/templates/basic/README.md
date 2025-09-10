# Basic Templates - Базовые шаблоны

## Описание
Простые шаблоны для начинающих пользователей n8n.

## Путь
`./templates/basic/`

## Доступные шаблоны

### 📄 [webhook_responder.json](./webhook_responder.json)
- **Описание**: Базовый webhook с ответом
- **Узлы**: Webhook → Respond to Webhook
- **Использование**: Прием данных через webhook
- **Сложность**: Простая (2 узла)

### 📄 [schedule_email.json](./schedule_email.json)
- **Описание**: Ежедневная отправка email
- **Узлы**: Schedule Trigger → Send Email → Log
- **Использование**: Автоматические уведомления
- **Сложность**: Простая (3 узла)

## Как использовать

### 1. Импорт шаблона
1. Откройте n8n
2. Нажмите "Import from File"
3. Выберите нужный JSON файл
4. Настройте credentials

### 2. Настройка
- Замените placeholder значения
- Настройте credentials
- Протестируйте процесс

### 3. Активация
- Включите процесс
- Проверьте выполнение
- Мониторьте логи

## Требования

### Для webhook_responder:
- Доступ к n8n
- Настроенный webhook URL

### Для schedule_email:
- Настроенные email credentials
- Доступ к SMTP серверу

## Примеры использования

### Webhook Responder:
```bash
curl -X POST https://your-n8n-instance.com/webhook/webhook \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello World"}'
```

### Schedule Email:
- Процесс автоматически запускается каждый день
- Отправляет email с текущей датой
- Логирует успешную отправку

---
*Последнее обновление: $(date)*

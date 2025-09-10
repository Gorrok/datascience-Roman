# Integrations - Интеграции с внешними сервисами

## Описание
Папка содержит процессы для интеграции с внешними API, сервисами и платформами.

## Путь
`./integrations/`

## Категории интеграций

### 📁 [crm/](./crm/)
- **Описание**: Интеграции с CRM системами
- **Сервисы**: Salesforce, HubSpot, Pipedrive, AmoCRM
- **Функции**: Синхронизация контактов, сделок, задач

### 📁 [email_services/](./email_services/)
- **Описание**: Интеграции с email сервисами
- **Сервисы**: Gmail, Outlook, Mailchimp, SendGrid
- **Функции**: Отправка, получение, обработка email

### 📁 [social_media/](./social_media/)
- **Описание**: Интеграции с социальными сетями
- **Сервисы**: Facebook, Twitter, LinkedIn, Instagram
- **Функции**: Публикация, мониторинг, аналитика

### 📁 [cloud_storage/](./cloud_storage/)
- **Описание**: Интеграции с облачными хранилищами
- **Сервисы**: Google Drive, Dropbox, OneDrive, AWS S3
- **Функции**: Загрузка, синхронизация, управление файлами

### 📁 [communication/](./communication/)
- **Описание**: Интеграции с коммуникационными платформами
- **Сервисы**: Slack, Discord, Teams, Zoom
- **Функции**: Уведомления, встречи, сообщения

### 📁 [ecommerce/](./ecommerce/)
- **Описание**: Интеграции с e-commerce платформами
- **Сервисы**: Shopify, WooCommerce, Magento, Stripe
- **Функции**: Заказы, платежи, инвентарь

## Типичные узлы для интеграций

### HTTP узлы:
- **HTTP Request** - базовые API запросы
- **Webhook** - прием входящих данных
- **OAuth2** - аутентификация

### Специализированные узлы:
- **Google Sheets** - работа с таблицами
- **Slack** - интеграция со Slack
- **Gmail** - работа с почтой
- **Salesforce** - CRM интеграция

## Лучшие практики

### 1. Аутентификация
```json
{
  "authentication": {
    "use_credentials": true,
    "store_secrets": "environment_variables",
    "refresh_tokens": true
  }
}
```

### 2. Обработка API ответов
- Всегда проверяйте статус код ответа
- Обрабатывайте ошибки API
- Используйте retry логику для временных сбоев

### 3. Rate Limiting
- Соблюдайте лимиты API
- Используйте задержки между запросами
- Реализуйте exponential backoff

### 4. Безопасность
- Никогда не храните секреты в коде
- Используйте переменные окружения
- Шифруйте чувствительные данные

## Частые ошибки

### ❌ Неправильная аутентификация
- **Проблема**: 401 Unauthorized ошибки
- **Решение**: Проверьте токены и credentials

### ❌ Превышение rate limits
- **Проблема**: 429 Too Many Requests
- **Решение**: Добавьте задержки и retry логику

### ❌ Неправильный формат данных
- **Проблема**: 400 Bad Request
- **Решение**: Валидируйте данные перед отправкой

### ❌ Таймауты
- **Проблема**: Запросы зависают
- **Решение**: Установите разумные таймауты

## Полезные ресурсы

### Документация API:
- [n8n HTTP Request Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [OAuth2 Authentication](https://docs.n8n.io/integrations/credentials/oauth2/)
- [Webhook Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)

### Тестирование API:
- [Postman](https://www.postman.com/) - тестирование API
- [Insomnia](https://insomnia.rest/) - альтернатива Postman
- [HTTPie](https://httpie.io/) - CLI для API

### Мониторинг:
- [API Status Pages](https://status.salesforce.com/) - статус сервисов
- [Uptime Robot](https://uptimerobot.com/) - мониторинг API

## Примеры интеграций

### Базовая HTTP интеграция:
```json
{
  "nodes": [
    {
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.example.com/data",
        "method": "GET",
        "headers": {
          "Authorization": "Bearer {{$credentials.apiKey}}"
        }
      }
    }
  ]
}
```

---
*Последнее обновление: $(date)*

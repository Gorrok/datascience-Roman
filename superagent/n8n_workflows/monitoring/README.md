# Monitoring - Мониторинг и логирование

## Описание
Папка содержит процессы для мониторинга работы системы, логирования и уведомлений о состоянии процессов.

## Путь
`./monitoring/`

## Категории мониторинга

### 📁 [alerts/](./alerts/)
- **Описание**: Система алертов и уведомлений
- **Функции**: Критические уведомления, эскалация
- **Каналы**: Email, Slack, SMS, Telegram

### 📁 [metrics/](./metrics/)
- **Описание**: Сбор и анализ метрик
- **Функции**: Производительность, использование ресурсов
- **Инструменты**: Prometheus, Grafana, InfluxDB

### 📁 [logs/](./logs/)
- **Описание**: Централизованное логирование
- **Функции**: Агрегация, анализ, поиск логов
- **Системы**: ELK Stack, Splunk, Fluentd

### 📁 [health_checks/](./health_checks/)
- **Описание**: Проверки состояния системы
- **Функции**: Ping, API health, database status
- **Частота**: Постоянно, по расписанию

### 📁 [reports/](./reports/)
- **Описание**: Автоматические отчеты
- **Функции**: Ежедневные, еженедельные, ежемесячные
- **Форматы**: PDF, Excel, HTML, JSON

## Типичные узлы для мониторинга

### Мониторинг:
- **HTTP Request** - проверка API endpoints
- **Schedule Trigger** - регулярные проверки
- **Webhook** - прием метрик

### Уведомления:
- **Email Send** - email уведомления
- **Slack** - уведомления в Slack
- **Telegram** - уведомления в Telegram

### Логирование:
- **Set** - добавление метаданных
- **Function** - форматирование логов
- **HTTP Request** - отправка в систему логирования

## Лучшие практики

### 1. Структурированное логирование
```json
{
  "log_format": {
    "timestamp": "ISO 8601",
    "level": "INFO|WARN|ERROR",
    "service": "service_name",
    "message": "human_readable_message",
    "context": {
      "user_id": "123",
      "request_id": "abc-def"
    }
  }
}
```

### 2. Мониторинг ключевых метрик
- **Доступность** - uptime сервисов
- **Производительность** - время ответа
- **Ошибки** - количество ошибок
- **Ресурсы** - CPU, память, диск

### 3. Настройка алертов
- Используйте пороговые значения
- Настройте эскалацию
- Группируйте похожие алерты

### 4. Дашборды
- Создавайте информативные дашборды
- Используйте цветовое кодирование
- Обновляйте данные в реальном времени

## Частые ошибки

### ❌ Слишком много алертов
- **Проблема**: Alert fatigue, игнорирование важных уведомлений
- **Решение**: Настройте приоритеты и фильтрацию

### ❌ Неструктурированные логи
- **Проблема**: Сложно анализировать и искать
- **Решение**: Используйте стандартные форматы

### ❌ Отсутствие контекста
- **Проблема**: Непонятно что произошло
- **Решение**: Добавляйте метаданные и контекст

### ❌ Неоптимизированные запросы
- **Проблема**: Медленная работа мониторинга
- **Решение**: Индексируйте логи, используйте агрегацию

## Полезные ресурсы

### Инструменты мониторинга:
- [Prometheus](https://prometheus.io/) - сбор метрик
- [Grafana](https://grafana.com/) - визуализация
- [ELK Stack](https://www.elastic.co/elk-stack) - логирование
- [Splunk](https://www.splunk.com/) - анализ данных

### Документация:
- [n8n Monitoring](https://docs.n8n.io/hosting/monitoring/)
- [Logging Best Practices](https://docs.n8n.io/workflows/logging/)
- [Error Handling](https://docs.n8n.io/workflows/error-handling/)

## Примеры мониторинга

### Health Check процесс:
```json
{
  "name": "API Health Check",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [{"field": "minutes", "minutesInterval": 5}]
        }
      }
    },
    {
      "name": "Check API",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "https://api.example.com/health",
        "method": "GET",
        "timeout": 10000
      }
    },
    {
      "name": "IF Status OK",
      "type": "n8n-nodes-base.if",
      "parameters": {
        "conditions": {
          "number": [{
            "value1": "={{ $json.status }}",
            "operation": "equal",
            "value2": 200
          }]
        }
      }
    }
  ]
}
```

### Логирование ошибок:
```javascript
// Function Node для логирования
const logEntry = {
  timestamp: new Date().toISOString(),
  level: 'ERROR',
  service: 'n8n-workflow',
  message: $json.message || 'Unknown error',
  context: {
    workflow_id: $workflow.id,
    execution_id: $execution.id,
    node_name: $node.name,
    error: $json.error
  }
};

// Отправка в систему логирования
return [{
  json: logEntry,
  binary: {}
}];
```

### Метрики производительности:
```javascript
// Function Node для сбора метрик
const startTime = Date.now();
const executionTime = startTime - $json.start_time;

const metrics = {
  timestamp: new Date().toISOString(),
  metric_name: 'workflow_execution_time',
  value: executionTime,
  tags: {
    workflow: $workflow.name,
    node: $node.name,
    status: $json.status
  }
};

return [{ json: metrics }];
```

---
*Последнее обновление: $(date)*

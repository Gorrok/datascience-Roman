# Troubleshooting - Решение проблем n8n

## Описание
Руководство по решению частых проблем и ошибок в n8n.

## Путь
`./documentation/troubleshooting/`

## Категории проблем

### 📁 [authentication/](./authentication/)
- **Описание**: Проблемы с аутентификацией
- **Примеры**: OAuth, API keys, credentials
- **Решения**: Настройка, обновление токенов

### 📁 [data_processing/](./data_processing/)
- **Описание**: Ошибки обработки данных
- **Примеры**: Форматы, валидация, трансформация
- **Решения**: Исправление данных, валидация

### 📁 [performance/](./performance/)
- **Описание**: Проблемы производительности
- **Примеры**: Медленная работа, таймауты
- **Решения**: Оптимизация, кэширование

### 📁 [integration/](./integration/)
- **Описание**: Ошибки интеграций
- **Примеры**: API, webhooks, внешние сервисы
- **Решения**: Настройка, обработка ошибок

## Частые ошибки и решения

### 🔐 Аутентификация

#### ❌ 401 Unauthorized
**Проблема**: Ошибка аутентификации
**Возможные причины**:
- Неправильный API ключ
- Истекший токен
- Неправильные credentials

**Решение**:
1. Проверьте API ключ в credentials
2. Обновите токен OAuth
3. Проверьте права доступа
4. Убедитесь в правильности URL

```javascript
// Проверка credentials
const credentials = $credentials.apiKey;
if (!credentials) {
  throw new Error('API key not found');
}
```

#### ❌ 403 Forbidden
**Проблема**: Недостаточно прав
**Решение**:
1. Проверьте scope разрешений
2. Обратитесь к администратору API
3. Обновите права доступа

### 📊 Обработка данных

#### ❌ Invalid JSON format
**Проблема**: Неправильный формат JSON
**Решение**:
```javascript
// Валидация JSON
try {
  const data = JSON.parse($json.raw_data);
  return { json: data };
} catch (error) {
  throw new Error('Invalid JSON format: ' + error.message);
}
```

#### ❌ Missing required fields
**Проблема**: Отсутствуют обязательные поля
**Решение**:
```javascript
// Проверка обязательных полей
const requiredFields = ['id', 'name', 'email'];
const missingFields = requiredFields.filter(field => !$json[field]);

if (missingFields.length > 0) {
  throw new Error(`Missing required fields: ${missingFields.join(', ')}`);
}
```

#### ❌ Data type mismatch
**Проблема**: Неправильный тип данных
**Решение**:
```javascript
// Преобразование типов
const data = {
  id: parseInt($json.id),
  price: parseFloat($json.price),
  is_active: $json.is_active === 'true'
};
```

### ⚡ Производительность

#### ❌ Timeout errors
**Проблема**: Превышение времени ожидания
**Решение**:
1. Увеличьте timeout в настройках узла
2. Оптимизируйте запросы
3. Используйте пагинацию
4. Разбивайте большие операции

```json
{
  "timeout": 30000,
  "retry": {
    "enabled": true,
    "max_attempts": 3,
    "backoff": "exponential"
  }
}
```

#### ❌ Memory issues
**Проблема**: Нехватка памяти
**Решение**:
1. Обрабатывайте данные батчами
2. Используйте streaming для больших файлов
3. Очищайте временные данные
4. Увеличьте память сервера

```javascript
// Обработка батчами
const batchSize = 100;
const items = $input.all();
const batches = [];

for (let i = 0; i < items.length; i += batchSize) {
  batches.push(items.slice(i, i + batchSize));
}

return batches;
```

### 🔗 Интеграции

#### ❌ API rate limiting
**Проблема**: Превышение лимитов API
**Решение**:
```javascript
// Обработка rate limiting
const response = await $http.request({
  url: 'https://api.example.com/data',
  method: 'GET'
});

if (response.status === 429) {
  const retryAfter = response.headers['retry-after'] || 60;
  await new Promise(resolve => setTimeout(resolve, retryAfter * 1000));
  // Повторить запрос
}
```

#### ❌ Webhook not receiving data
**Проблема**: Webhook не получает данные
**Решение**:
1. Проверьте URL webhook
2. Убедитесь в доступности сервера
3. Проверьте SSL сертификат
4. Настройте правильные заголовки

```json
{
  "webhook": {
    "path": "webhook",
    "httpMethod": "POST",
    "responseMode": "responseNode",
    "options": {
      "noResponseBody": false
    }
  }
}
```

#### ❌ Database connection issues
**Проблема**: Проблемы с подключением к БД
**Решение**:
1. Проверьте строку подключения
2. Убедитесь в доступности БД
3. Проверьте права доступа
4. Настройте connection pooling

### 🔄 Workflow execution

#### ❌ Workflow not triggering
**Проблема**: Workflow не запускается
**Решение**:
1. Проверьте настройки триггера
2. Убедитесь в активности workflow
3. Проверьте cron выражение
4. Проверьте логи выполнения

#### ❌ Infinite loops
**Проблема**: Бесконечные циклы
**Решение**:
```javascript
// Защита от бесконечных циклов
const maxIterations = 100;
let iteration = 0;

while (condition && iteration < maxIterations) {
  // Логика цикла
  iteration++;
}

if (iteration >= maxIterations) {
  throw new Error('Maximum iterations reached');
}
```

#### ❌ Deadlocks
**Проблема**: Взаимные блокировки
**Решение**:
1. Избегайте циклических зависимостей
2. Используйте асинхронную обработку
3. Настройте таймауты
4. Мониторьте выполнение

## Диагностика проблем

### 1. Анализ логов
```javascript
// Структурированное логирование
const logEntry = {
  timestamp: new Date().toISOString(),
  level: 'ERROR',
  workflow: $workflow.name,
  node: $node.name,
  error: $json.error,
  context: $json.context
};

console.log(JSON.stringify(logEntry));
```

### 2. Мониторинг производительности
```javascript
// Измерение времени выполнения
const startTime = Date.now();
// ... выполнение операции ...
const executionTime = Date.now() - startTime;

if (executionTime > 5000) {
  console.warn(`Slow execution: ${executionTime}ms`);
}
```

### 3. Проверка состояния системы
```javascript
// Health check
const healthCheck = {
  timestamp: new Date().toISOString(),
  status: 'healthy',
  checks: {
    database: await checkDatabase(),
    api: await checkAPI(),
    memory: process.memoryUsage()
  }
};
```

## Инструменты диагностики

### 1. Встроенные инструменты n8n
- **Execution Logs** - логи выполнения
- **Node Inspector** - отладка узлов
- **Test Mode** - тестирование

### 2. Внешние инструменты
- **Postman** - тестирование API
- **curl** - командная строка
- **Browser DevTools** - отладка webhooks

### 3. Мониторинг
- **Prometheus** - метрики
- **Grafana** - визуализация
- **ELK Stack** - логирование

## Профилактика проблем

### 1. Тестирование
- Тестируйте на малых данных
- Проверяйте все ветки выполнения
- Используйте тестовые окружения

### 2. Мониторинг
- Настройте алерты
- Мониторьте производительность
- Отслеживайте ошибки

### 3. Документация
- Документируйте процессы
- Ведите changelog
- Записывайте решения проблем

### 4. Резервное копирование
- Регулярно создавайте бэкапы
- Тестируйте восстановление
- Храните конфигурации

## Полезные ресурсы

### Документация:
- [n8n Error Handling](https://docs.n8n.io/workflows/error-handling/)
- [n8n Debugging](https://docs.n8n.io/workflows/debugging/)
- [n8n Monitoring](https://docs.n8n.io/hosting/monitoring/)

### Сообщество:
- [n8n Community Forum](https://community.n8n.io/)
- [n8n GitHub Issues](https://github.com/n8n-io/n8n/issues)
- [n8n Discord](https://discord.gg/n8n)

### Инструменты:
- [n8n Workflow Designer](https://n8n.io/workflow-designer/)
- [JSON Validator](https://jsonlint.com/)
- [Cron Expression Generator](https://crontab.guru/)

---
*Последнее обновление: $(date)*

# Integration Issues - Проблемы интеграций

## Описание
Решенные задачи связанные с интеграциями с внешними API, сервисами и системами.

## Путь
`./documentation/solved_issues/integration_issues/`

## Решенные задачи

### ISSUE-006: API rate limiting - превышение лимитов запросов

#### Проблема
API возвращает ошибку 429 Too Many Requests при превышении лимитов запросов.

#### Симптомы
- Ошибка 429 Too Many Requests
- Процесс падает
- Данные не обрабатываются

#### Ошибки
```
HTTP 429 Too Many Requests
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded. Try again in 60 seconds."
}
```

#### Причина
Превышен лимит запросов к API (requests per minute/hour).

#### Решение
1. Добавьте задержки между запросами
2. Используйте retry логику с exponential backoff
3. Обрабатывайте заголовки rate limiting

#### Код решения
```javascript
// Обработка rate limiting
const makeApiRequest = async (url, options = {}) => {
  const maxRetries = 3;
  let retryCount = 0;
  
  while (retryCount < maxRetries) {
    try {
      const response = await $http.request({
        url,
        ...options,
        headers: {
          'User-Agent': 'n8n-workflow/1.0',
          ...options.headers
        }
      });
      
      return response;
    } catch (error) {
      if (error.status === 429) {
        retryCount++;
        
        // Получаем время ожидания из заголовков
        const retryAfter = error.headers['retry-after'] || 
                          error.headers['X-RateLimit-Reset'] ||
                          60;
        
        const waitTime = Math.min(retryAfter * 1000, 300000); // Максимум 5 минут
        
        console.log(`Rate limit exceeded. Waiting ${waitTime/1000} seconds...`);
        await new Promise(resolve => setTimeout(resolve, waitTime));
        
        continue;
      }
      
      throw error;
    }
  }
  
  throw new Error('Max retries exceeded for rate limiting');
};

// Использование с задержками
const processItems = async (items) => {
  const results = [];
  
  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    
    try {
      const response = await makeApiRequest(`https://api.example.com/process`, {
        method: 'POST',
        body: item
      });
      
      results.push(response);
      
      // Добавляем задержку между запросами
      if (i < items.length - 1) {
        await new Promise(resolve => setTimeout(resolve, 1000)); // 1 секунда
      }
      
    } catch (error) {
      console.error(`Error processing item ${i}:`, error.message);
      results.push({ error: error.message, item });
    }
  }
  
  return results;
};
```

#### Профилактика
- Соблюдайте лимиты API
- Используйте задержки между запросами
- Мониторьте использование API

#### Связанные задачи
- ISSUE-007: Таймауты API запросов
- ISSUE-008: Webhook не получает данные

#### Теги
`rate_limiting`, `429`, `api`, `retry`, `backoff`

#### Дата решения
2024-01-20

#### Автор решения
n8n Agent

---

### ISSUE-007: Таймауты API запросов

#### Проблема
API запросы превышают время ожидания и падают с ошибкой timeout.

#### Симптомы
- Ошибка timeout
- Медленная работа API
- Процесс зависает

#### Ошибки
```
TimeoutError: Request timeout after 30000ms
```

#### Причина
API сервер медленно отвечает или недоступен.

#### Решение
1. Увеличьте timeout для медленных API
2. Используйте retry логику
3. Добавьте fallback сценарии

#### Код решения
```javascript
// Настройка таймаутов и retry
const makeApiRequestWithTimeout = async (url, options = {}) => {
  const defaultTimeout = 30000; // 30 секунд
  const maxRetries = 3;
  let retryCount = 0;
  
  while (retryCount < maxRetries) {
    try {
      const response = await $http.request({
        url,
        timeout: options.timeout || defaultTimeout,
        ...options,
        headers: {
          'Connection': 'keep-alive',
          'Keep-Alive': 'timeout=5, max=1000',
          ...options.headers
        }
      });
      
      return response;
    } catch (error) {
      if (error.code === 'TIMEOUT' || error.message.includes('timeout')) {
        retryCount++;
        
        if (retryCount < maxRetries) {
          const backoffTime = Math.pow(2, retryCount) * 1000; // Exponential backoff
          console.log(`Timeout occurred. Retrying in ${backoffTime}ms...`);
          await new Promise(resolve => setTimeout(resolve, backoffTime));
          continue;
        }
      }
      
      throw error;
    }
  }
  
  throw new Error('Max retries exceeded for timeout');
};

// Адаптивные таймауты
const getAdaptiveTimeout = (baseTimeout, retryCount) => {
  return Math.min(baseTimeout * Math.pow(1.5, retryCount), 120000); // Максимум 2 минуты
};
```

#### Профилактика
- Устанавливайте разумные таймауты
- Используйте retry логику
- Мониторьте производительность API

#### Связанные задачи
- ISSUE-006: Rate limiting
- ISSUE-009: Нестабильное соединение

#### Теги
`timeout`, `api`, `retry`, `performance`

#### Дата решения
2024-01-21

#### Автор решения
n8n Agent

---

## Статистика категории

### Всего решенных задач: 2
### Последнее обновление: 2024-01-21

## Полезные ресурсы

### Документация:
- [n8n HTTP Request](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/)
- [n8n Webhook](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.webhook/)

### Инструменты:
- [Postman](https://www.postman.com/) - тестирование API
- [Insomnia](https://insomnia.rest/) - альтернатива Postman

---
*Категория постоянно обновляется новыми решениями*
*Последнее обновление: $(date)*

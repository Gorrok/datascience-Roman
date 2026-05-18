# Error Handling Templates - Шаблоны обработки ошибок

## Описание
Шаблоны для надежной обработки ошибок в n8n процессах.

## Путь
`./templates/error_handling/`

## Доступные шаблоны

### 📄 [retry_with_fallback.json](./retry_with_fallback.json)
- **Описание**: Retry логика с fallback сценарием
- **Узлы**: Webhook → API Call → Check Status → Success/Fallback Response
- **Использование**: Надежные API вызовы
- **Сложность**: Средняя (5 узлов)

## Паттерны обработки ошибок

### 1. Retry Pattern
```json
{
  "retry": {
    "enabled": true,
    "maxAttempts": 3,
    "backoff": "exponential"
  }
}
```

### 2. Fallback Pattern
```javascript
// Проверка статуса ответа
if ($json.status === 200) {
  return { json: $json };
} else {
  // Fallback логика
  return { json: { fallback: true, data: $json } };
}
```

### 3. Error Notification Pattern
```javascript
// Уведомление об ошибке
const errorNotification = {
  level: 'error',
  message: 'Process failed',
  context: {
    workflow: $workflow.name,
    error: $json.error,
    timestamp: new Date().toISOString()
  }
};
```

## Лучшие практики

### 1. Всегда обрабатывайте ошибки
- Используйте Error Trigger узлы
- Добавляйте fallback сценарии
- Логируйте ошибки

### 2. Настройте retry логику
- Используйте exponential backoff
- Ограничивайте количество попыток
- Мониторьте retry метрики

### 3. Уведомляйте об ошибках
- Настройте алерты
- Используйте разные каналы
- Группируйте похожие ошибки

## Примеры использования

### Retry с Fallback:
1. API вызов с retry логикой
2. Проверка статуса ответа
3. Успешный ответ или fallback
4. Уведомление о результате

### Обработка таймаутов:
```javascript
// Обработка таймаутов
try {
  const response = await $http.request({
    url: 'https://api.example.com/data',
    timeout: 10000
  });
  return { json: response };
} catch (error) {
  if (error.code === 'TIMEOUT') {
    return { json: { error: 'timeout', fallback: true } };
  }
  throw error;
}
```

## Мониторинг ошибок

### 1. Логирование
- Структурированные логи
- Контекст ошибок
- Временные метки

### 2. Метрики
- Количество ошибок
- Время восстановления
- Частота retry

### 3. Алерты
- Критические ошибки
- Превышение порогов
- Необычные паттерны

---
*Последнее обновление: $(date)*

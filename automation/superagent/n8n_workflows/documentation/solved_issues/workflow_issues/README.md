# Workflow Issues - Проблемы выполнения процессов

## Описание
Решенные задачи связанные с выполнением, логикой и ошибками n8n процессов.

## Путь
`./documentation/solved_issues/workflow_issues/`

## Решенные задачи

### ISSUE-010: Workflow не запускается по расписанию

#### Проблема
Workflow с Schedule Trigger не запускается в назначенное время.

#### Симптомы
- Процесс не выполняется
- Нет логов выполнения
- Расписание настроено правильно

#### Ошибки
```
No execution logs found
Schedule trigger not firing
```

#### Причина
Workflow неактивен или неправильно настроен Schedule Trigger.

#### Решение
1. Проверьте активность workflow
2. Убедитесь в правильности cron выражения
3. Проверьте настройки триггера

#### Код решения
```javascript
// Проверка настроек Schedule Trigger
const validateScheduleTrigger = (cronExpression) => {
  // Проверяем формат cron
  const cronRegex = /^(\*|([0-5]?\d)) (\*|([01]?\d|2[0-3])) (\*|([012]?\d|3[01])) (\*|([0]?\d|1[0-2])) (\*|([0-6]))$/;
  
  if (!cronRegex.test(cronExpression)) {
    throw new Error('Invalid cron expression format');
  }
  
  // Проверяем, что не все поля равны *
  const parts = cronExpression.split(' ');
  if (parts.every(part => part === '*')) {
    throw new Error('Cron expression cannot be all asterisks');
  }
  
  return true;
};

// Тестирование расписания
const testSchedule = (cronExpression) => {
  try {
    validateScheduleTrigger(cronExpression);
    
    // Логируем следующее время выполнения
    const nextRun = getNextRunTime(cronExpression);
    console.log(`Next scheduled run: ${nextRun}`);
    
    return { valid: true, nextRun };
  } catch (error) {
    return { valid: false, error: error.message };
  }
};

// Использование
const cronExpression = '0 9 * * 1-5'; // Каждый день в 9:00, кроме выходных
const result = testSchedule(cronExpression);
```

#### Профилактика
- Тестируйте cron выражения
- Проверяйте активность workflow
- Мониторьте выполнение

#### Связанные задачи
- ISSUE-011: Webhook не получает данные
- ISSUE-012: Условия не работают

#### Теги
`schedule`, `trigger`, `cron`, `workflow`, `execution`

#### Дата решения
2024-01-24

#### Автор решения
n8n Agent

---

### ISSUE-011: Условия IF не работают правильно

#### Проблема
Узел IF не срабатывает или работает неправильно.

#### Симптомы
- Неправильная ветка выполнения
- Условие не срабатывает
- Неожиданное поведение

#### Ошибы
```
Condition not met when it should be
Wrong branch executed
```

#### Причина
Неправильная настройка условий или типов данных.

#### Решение
1. Проверьте типы данных
2. Убедитесь в правильности операторов
3. Добавьте логирование

#### Код решения
```javascript
// Безопасная проверка условий
const safeConditionCheck = (value1, operator, value2) => {
  try {
    // Нормализуем типы данных
    const normalizedValue1 = normalizeValue(value1);
    const normalizedValue2 = normalizeValue(value2);
    
    switch (operator) {
      case 'equal':
        return normalizedValue1 === normalizedValue2;
      case 'notEqual':
        return normalizedValue1 !== normalizedValue2;
      case 'greaterThan':
        return Number(normalizedValue1) > Number(normalizedValue2);
      case 'lessThan':
        return Number(normalizedValue1) < Number(normalizedValue2);
      case 'contains':
        return String(normalizedValue1).includes(String(normalizedValue2));
      case 'notContains':
        return !String(normalizedValue1).includes(String(normalizedValue2));
      case 'startsWith':
        return String(normalizedValue1).startsWith(String(normalizedValue2));
      case 'endsWith':
        return String(normalizedValue1).endsWith(String(normalizedValue2));
      case 'isEmpty':
        return !normalizedValue1 || normalizedValue1 === '';
      case 'isNotEmpty':
        return normalizedValue1 && normalizedValue1 !== '';
      default:
        throw new Error(`Unknown operator: ${operator}`);
    }
  } catch (error) {
    console.error('Condition check error:', error.message);
    return false;
  }
};

// Нормализация значений
const normalizeValue = (value) => {
  if (value === null || value === undefined) {
    return '';
  }
  
  if (typeof value === 'string') {
    return value.trim();
  }
  
  if (typeof value === 'number') {
    return value;
  }
  
  if (typeof value === 'boolean') {
    return value;
  }
  
  return String(value);
};

// Логирование условий
const logCondition = (value1, operator, value2, result) => {
  console.log(`Condition: ${value1} ${operator} ${value2} = ${result}`);
  return result;
};

// Использование
const value1 = $json.status;
const operator = 'equal';
const value2 = 'active';

const result = safeConditionCheck(value1, operator, value2);
logCondition(value1, operator, value2, result);

return { json: { condition_result: result } };
```

#### Профилактика
- Проверяйте типы данных
- Используйте безопасные операторы
- Добавляйте логирование

#### Связанные задачи
- ISSUE-010: Schedule Trigger
- ISSUE-013: Циклы и итерации

#### Теги
`if`, `conditions`, `logic`, `workflow`, `operators`

#### Дата решения
2024-01-25

#### Автор решения
n8n Agent

---

### ISSUE-012: Бесконечные циклы в процессах

#### Проблема
Процесс попадает в бесконечный цикл и не может завершиться.

#### Симптомы
- Процесс выполняется бесконечно
- Высокое потребление ресурсов
- Система зависает

#### Ошибки
```
Infinite loop detected
Maximum execution time exceeded
```

#### Причина
Отсутствие условий выхода из цикла или неправильная логика.

#### Решение
1. Добавьте счетчики итераций
2. Установите максимальное количество итераций
3. Добавьте условия выхода

#### Код решения
```javascript
// Защита от бесконечных циклов
const safeLoop = (items, maxIterations = 1000) => {
  const results = [];
  let iteration = 0;
  
  for (const item of items) {
    iteration++;
    
    // Проверяем лимит итераций
    if (iteration > maxIterations) {
      console.warn(`Maximum iterations (${maxIterations}) reached. Breaking loop.`);
      break;
    }
    
    try {
      const result = processItem(item);
      results.push(result);
      
      // Логируем прогресс
      if (iteration % 100 === 0) {
        console.log(`Processed ${iteration} items`);
      }
      
    } catch (error) {
      console.error(`Error processing item ${iteration}:`, error.message);
      results.push({ error: error.message, item });
    }
  }
  
  return results;
};

// Рекурсивная обработка с защитой
const safeRecursiveProcess = (data, maxDepth = 10, currentDepth = 0) => {
  if (currentDepth >= maxDepth) {
    console.warn(`Maximum recursion depth (${maxDepth}) reached.`);
    return data;
  }
  
  if (Array.isArray(data)) {
    return data.map(item => safeRecursiveProcess(item, maxDepth, currentDepth + 1));
  }
  
  if (typeof data === 'object' && data !== null) {
    const result = {};
    for (const [key, value] of Object.entries(data)) {
      result[key] = safeRecursiveProcess(value, maxDepth, currentDepth + 1);
    }
    return result;
  }
  
  return data;
};

// Использование
const items = $input.all();
const maxIterations = 500;

const results = safeLoop(items, maxIterations);
return results;
```

#### Профилактика
- Всегда устанавливайте лимиты итераций
- Добавляйте условия выхода
- Мониторьте выполнение

#### Связанные задачи
- ISSUE-011: Условия IF
- ISSUE-014: Рекурсивные процессы

#### Теги
`infinite_loop`, `recursion`, `iteration`, `performance`, `safety`

#### Дата решения
2024-01-26

#### Автор решения
n8n Agent

---

## Статистика категории

### Всего решенных задач: 3
### Последнее обновление: 2024-01-26

## Полезные ресурсы

### Документация:
- [n8n Workflows](https://docs.n8n.io/workflows/)
- [n8n Triggers](https://docs.n8n.io/integrations/builtin/trigger-nodes/)

### Инструменты:
- [Cron Expression Generator](https://crontab.guru/)
- [JSONPath Tester](https://jsonpath.com/)

---
*Категория постоянно обновляется новыми решениями*
*Последнее обновление: $(date)*

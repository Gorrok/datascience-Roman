# Performance Issues - Проблемы производительности

## Описание
Решенные задачи связанные с производительностью, оптимизацией и масштабированием n8n процессов.

## Путь
`./documentation/solved_issues/performance_issues/`

## Решенные задачи

### ISSUE-008: Медленная обработка больших объемов данных

#### Проблема
Процесс работает очень медленно при обработке больших массивов данных.

#### Симптомы
- Процесс выполняется очень долго
- Высокое потребление памяти
- Таймауты выполнения

#### Ошибки
```
Execution timeout after 300000ms
Memory usage exceeded 512MB
```

#### Причина
Обработка всех данных в одном цикле без оптимизации.

#### Решение
1. Используйте батчевую обработку
2. Применяйте пагинацию
3. Оптимизируйте алгоритмы

#### Код решения
```javascript
// Батчевая обработка данных
const processDataInBatches = (items, batchSize = 100) => {
  const batches = [];
  
  for (let i = 0; i < items.length; i += batchSize) {
    batches.push(items.slice(i, i + batchSize));
  }
  
  return batches;
};

// Обработка с пагинацией
const processWithPagination = async (totalItems, pageSize = 50) => {
  const results = [];
  const totalPages = Math.ceil(totalItems / pageSize);
  
  for (let page = 1; page <= totalPages; page++) {
    console.log(`Processing page ${page} of ${totalPages}`);
    
    const startIndex = (page - 1) * pageSize;
    const endIndex = Math.min(startIndex + pageSize, totalItems);
    
    const batch = items.slice(startIndex, endIndex);
    const processedBatch = await processBatch(batch);
    
    results.push(...processedBatch);
    
    // Добавляем небольшую задержку между батчами
    if (page < totalPages) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  return results;
};

// Оптимизированная обработка
const processBatch = async (batch) => {
  return batch.map(item => {
    // Оптимизированная логика обработки
    return {
      id: item.id,
      processed_at: new Date().toISOString(),
      result: performOptimizedOperation(item)
    };
  });
};

// Использование
const items = $input.all();
const batchSize = 100;

if (items.length > batchSize) {
  const batches = processDataInBatches(items, batchSize);
  const results = [];
  
  for (const batch of batches) {
    const processedBatch = await processBatch(batch);
    results.push(...processedBatch);
  }
  
  return results;
} else {
  return await processBatch(items);
}
```

#### Профилактика
- Используйте батчевую обработку
- Применяйте пагинацию
- Мониторьте потребление памяти

#### Связанные задачи
- ISSUE-009: Высокое потребление памяти
- ISSUE-010: Медленные API запросы

#### Теги
`performance`, `batch_processing`, `pagination`, `memory`, `optimization`

#### Дата решения
2024-01-22

#### Автор решения
n8n Agent

---

### ISSUE-009: Высокое потребление памяти

#### Проблема
Процесс потребляет слишком много памяти и может привести к сбою системы.

#### Симптомы
- Высокое потребление RAM
- Медленная работа системы
- Возможные сбои

#### Ошибки
```
Memory usage exceeded 1GB
Out of memory error
```

#### Причина
Накопление данных в памяти без очистки.

#### Решение
1. Очищайте временные данные
2. Используйте streaming для больших файлов
3. Оптимизируйте структуры данных

#### Код решения
```javascript
// Оптимизированная обработка с очисткой памяти
const processDataWithMemoryOptimization = (items) => {
  const results = [];
  const batchSize = 50;
  
  for (let i = 0; i < items.length; i += batchSize) {
    const batch = items.slice(i, i + batchSize);
    
    // Обрабатываем батч
    const processedBatch = batch.map(item => {
      const result = {
        id: item.id,
        processed_at: new Date().toISOString(),
        data: processItem(item)
      };
      
      // Очищаем исходный объект
      delete item.tempData;
      delete item.cache;
      
      return result;
    });
    
    results.push(...processedBatch);
    
    // Принудительная очистка памяти
    if (global.gc) {
      global.gc();
    }
    
    // Логируем использование памяти
    const memUsage = process.memoryUsage();
    console.log(`Memory usage: ${Math.round(memUsage.heapUsed / 1024 / 1024)}MB`);
  }
  
  return results;
};

// Streaming обработка файлов
const processFileStream = (filePath) => {
  const fs = require('fs');
  const readline = require('readline');
  
  return new Promise((resolve, reject) => {
    const results = [];
    const fileStream = fs.createReadStream(filePath);
    const rl = readline.createInterface({
      input: fileStream,
      crlfDelay: Infinity
    });
    
    rl.on('line', (line) => {
      try {
        const data = JSON.parse(line);
        const processed = processItem(data);
        results.push(processed);
        
        // Ограничиваем размер результатов
        if (results.length > 1000) {
          results.shift(); // Удаляем старые элементы
        }
      } catch (error) {
        console.error('Error processing line:', error.message);
      }
    });
    
    rl.on('close', () => {
      resolve(results);
    });
    
    rl.on('error', reject);
  });
};
```

#### Профилактика
- Мониторьте потребление памяти
- Используйте streaming для больших файлов
- Очищайте временные данные

#### Связанные задачи
- ISSUE-008: Медленная обработка
- ISSUE-011: Оптимизация алгоритмов

#### Теги
`memory`, `performance`, `optimization`, `streaming`, `gc`

#### Дата решения
2024-01-23

#### Автор решения
n8n Agent

---

## Статистика категории

### Всего решенных задач: 2
### Последнее обновление: 2024-01-23

## Полезные ресурсы

### Документация:
- [n8n Performance](https://docs.n8n.io/hosting/performance/)
- [n8n Monitoring](https://docs.n8n.io/hosting/monitoring/)

### Инструменты:
- [Node.js Memory Profiler](https://nodejs.org/en/docs/guides/simple-profiling/)
- [Chrome DevTools](https://developers.google.com/web/tools/chrome-devtools)

---
*Категория постоянно обновляется новыми решениями*
*Последнее обновление: $(date)*

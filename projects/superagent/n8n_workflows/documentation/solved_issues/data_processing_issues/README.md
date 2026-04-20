# Data Processing Issues - Проблемы обработки данных

## Описание
Решенные задачи связанные с обработкой, трансформацией и валидацией данных в n8n.

## Путь
`./documentation/solved_issues/data_processing_issues/`

## Решенные задачи

### ISSUE-003: JSON парсинг падает на невалидных данных

#### Проблема
Процесс падает при попытке парсинга невалидного JSON.

#### Симптомы
- Ошибка "Unexpected token"
- Процесс останавливается
- Данные не обрабатываются

#### Ошибки
```
SyntaxError: Unexpected token } in JSON at position 123
```

#### Причина
Входящие данные содержат невалидный JSON или повреждены.

#### Решение
1. Добавьте валидацию JSON перед парсингом
2. Используйте try-catch для обработки ошибок
3. Предоставьте fallback для невалидных данных

#### Код решения
```javascript
// Безопасный парсинг JSON
const parseJsonSafely = (jsonString) => {
  try {
    // Очистка от лишних символов
    const cleaned = jsonString.trim();
    
    // Проверка на пустую строку
    if (!cleaned) {
      return null;
    }
    
    // Парсинг JSON
    const parsed = JSON.parse(cleaned);
    return parsed;
  } catch (error) {
    console.error('JSON parsing error:', error.message);
    
    // Попытка исправить распространенные ошибки
    try {
      const fixed = jsonString
        .replace(/,(\s*[}\]])/g, '$1') // Убираем лишние запятые
        .replace(/([{,]\s*)(\w+):/g, '$1"$2":'); // Добавляем кавычки к ключам
      
      return JSON.parse(fixed);
    } catch (secondError) {
      // Возвращаем null для неисправимых данных
      return null;
    }
  }
};

// Использование
const data = parseJsonSafely($json.raw_data);
if (data) {
  return { json: data };
} else {
  return { json: { error: 'Invalid JSON data', raw: $json.raw_data } };
}
```

#### Профилактика
- Валидируйте данные на входе
- Используйте схемы валидации
- Добавляйте логирование ошибок

#### Связанные задачи
- ISSUE-004: CSV парсинг с неправильной кодировкой
- ISSUE-005: Обработка null значений

#### Теги
`json`, `parsing`, `validation`, `error_handling`

#### Дата решения
2024-01-17

#### Автор решения
n8n Agent

---

### ISSUE-004: CSV файл с неправильной кодировкой

#### Проблема
CSV файл содержит символы в неправильной кодировке, что приводит к ошибкам обработки.

#### Симптомы
- Неправильное отображение символов
- Ошибки при обработке данных
- Проблемы с кириллицей

#### Ошибки
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd0 in position 15
```

#### Причина
CSV файл сохранен в кодировке отличной от UTF-8 (например, Windows-1251).

#### Решение
1. Определите кодировку файла
2. Конвертируйте в UTF-8
3. Обработайте данные

#### Код решения
```javascript
// Определение и конвертация кодировки
const detectAndConvertEncoding = (buffer) => {
  const encodings = ['utf-8', 'windows-1251', 'iso-8859-1', 'cp1252'];
  
  for (const encoding of encodings) {
    try {
      const text = buffer.toString(encoding);
      // Проверяем, что текст содержит валидные символы
      if (text.includes('') === false) {
        return { text, encoding };
      }
    } catch (error) {
      continue;
    }
  }
  
  // Fallback на UTF-8 с заменой невалидных символов
  return { 
    text: buffer.toString('utf-8').replace(/\uFFFD/g, '?'), 
    encoding: 'utf-8-fallback' 
  };
};

// Обработка CSV файла
const processCsvFile = (binaryData) => {
  const buffer = Buffer.from(binaryData, 'base64');
  const { text, encoding } = detectAndConvertEncoding(buffer);
  
  const lines = text.split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  
  const result = lines.slice(1).map((line, index) => {
    const values = line.split(',').map(v => v.trim());
    const obj = {};
    
    headers.forEach((header, i) => {
      obj[header] = values[i] || '';
    });
    
    return {
      ...obj,
      _row_number: index + 2,
      _encoding: encoding
    };
  });
  
  return result;
};

// Использование
const csvData = $input.first().binary.data;
const processedData = processCsvFile(csvData);
return processedData;
```

#### Профилактика
- Указывайте кодировку при создании файлов
- Используйте UTF-8 по умолчанию
- Добавляйте BOM для UTF-8 файлов

#### Связанные задачи
- ISSUE-003: JSON парсинг
- ISSUE-006: Обработка больших файлов

#### Теги
`csv`, `encoding`, `utf-8`, `windows-1251`, `file_processing`

#### Дата решения
2024-01-18

#### Автор решения
n8n Agent

---

### ISSUE-005: Обработка null и undefined значений

#### Проблема
Процесс падает при обработке данных с null или undefined значениями.

#### Симптомы
- Ошибка "Cannot read property of null"
- Процесс останавливается
- Неожиданное поведение

#### Ошибки
```
TypeError: Cannot read property 'name' of null
```

#### Причина
Данные содержат null или undefined значения, которые не обрабатываются корректно.

#### Решение
1. Добавьте проверки на null/undefined
2. Используйте значения по умолчанию
3. Обрабатывайте пустые значения

#### Код решения
```javascript
// Безопасная обработка данных
const safeGet = (obj, path, defaultValue = null) => {
  try {
    const keys = path.split('.');
    let result = obj;
    
    for (const key of keys) {
      if (result === null || result === undefined) {
        return defaultValue;
      }
      result = result[key];
    }
    
    return result !== null && result !== undefined ? result : defaultValue;
  } catch (error) {
    return defaultValue;
  }
};

// Обработка данных с проверками
const processData = (item) => {
  return {
    id: safeGet(item, 'id', 'unknown'),
    name: safeGet(item, 'name', 'No Name'),
    email: safeGet(item, 'contact.email', 'no-email@example.com'),
    phone: safeGet(item, 'contact.phone', ''),
    created_at: safeGet(item, 'metadata.created_at', new Date().toISOString()),
    is_active: safeGet(item, 'status.is_active', false),
    tags: safeGet(item, 'tags', []),
    // Обработка массивов
    items: Array.isArray(item.items) ? item.items : [],
    // Обработка объектов
    settings: typeof item.settings === 'object' ? item.settings : {}
  };
};

// Использование
const items = $input.all();
const processedItems = items.map(item => processData(item.json));
return processedItems;
```

#### Профилактика
- Всегда проверяйте данные на null/undefined
- Используйте значения по умолчанию
- Валидируйте структуру данных

#### Связанные задачи
- ISSUE-003: JSON парсинг
- ISSUE-007: Валидация данных

#### Теги
`null`, `undefined`, `validation`, `data_processing`, `error_handling`

#### Дата решения
2024-01-19

#### Автор решения
n8n Agent

---

## Статистика категории

### Всего решенных задач: 3
### Последнее обновление: 2024-01-19

## Полезные ресурсы

### Документация:
- [n8n Data Processing](https://docs.n8n.io/workflows/data-processing/)
- [JSON Processing](https://docs.n8n.io/workflows/data-processing/json/)

### Инструменты:
- [JSON Validator](https://jsonlint.com/)
- [CSV Validator](https://csvlint.io/)

---
*Категория постоянно обновляется новыми решениями*
*Последнее обновление: $(date)*

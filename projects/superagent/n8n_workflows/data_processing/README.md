# Data Processing - Обработка и трансформация данных

## Описание
Папка содержит процессы для обработки, трансформации и анализа данных различных форматов.

## Путь
`./data_processing/`

## Категории обработки данных

### 📁 [etl/](./etl/)
- **Описание**: Extract, Transform, Load процессы
- **Функции**: Извлечение, трансформация, загрузка данных
- **Источники**: Базы данных, API, файлы

### 📁 [validation/](./validation/)
- **Описание**: Валидация и проверка данных
- **Функции**: Проверка форматов, обязательных полей
- **Типы**: Email, телефон, даты, числовые значения

### 📁 [transformation/](./transformation/)
- **Описание**: Трансформация данных
- **Функции**: Форматирование, нормализация, агрегация
- **Форматы**: JSON, CSV, XML, Excel

### 📁 [cleaning/](./cleaning/)
- **Описание**: Очистка и нормализация данных
- **Функции**: Удаление дубликатов, исправление ошибок
- **Процессы**: Дедупликация, стандартизация

### 📁 [analytics/](./analytics/)
- **Описание**: Аналитика и отчетность
- **Функции**: Агрегация, группировка, статистика
- **Выводы**: Графики, таблицы, дашборды

## Типичные узлы для обработки данных

### Обработка данных:
- **Set** - установка значений
- **Code** - выполнение JavaScript/Python кода
- **Function** - пользовательские функции
- **Item Lists** - работа со списками

### Трансформация:
- **Move Binary Data** - работа с бинарными данными
- **Convert to File** - конвертация в файлы
- **Extract from File** - извлечение из файлов

### Валидация:
- **IF** - условная логика
- **Switch** - множественные условия
- **Merge** - объединение данных

## Лучшие практики

### 1. Структурирование данных
```json
{
  "data_structure": {
    "standardize_format": true,
    "validate_required_fields": true,
    "handle_null_values": true
  }
}
```

### 2. Обработка больших объемов
- Используйте пагинацию
- Обрабатывайте данные батчами
- Применяйте фильтрацию на раннем этапе

### 3. Обработка ошибок
- Валидируйте данные на входе
- Обрабатывайте исключения
- Логируйте ошибки обработки

### 4. Производительность
- Минимизируйте количество узлов
- Используйте эффективные алгоритмы
- Кэшируйте результаты

## Частые ошибки

### ❌ Неправильная обработка null значений
- **Проблема**: Ошибки при обработке пустых значений
- **Решение**: Всегда проверяйте на null/undefined

### ❌ Неэффективная обработка больших данных
- **Проблема**: Медленная работа с большими массивами
- **Решение**: Используйте батчинг и пагинацию

### ❌ Отсутствие валидации
- **Проблема**: Неожиданные форматы данных
- **Решение**: Валидируйте данные на каждом этапе

### ❌ Проблемы с кодировкой
- **Проблема**: Неправильное отображение символов
- **Решение**: Указывайте кодировку явно

## Полезные ресурсы

### Документация:
- [Data Processing Nodes](https://docs.n8n.io/integrations/builtin/core-nodes/)
- [Code Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.code/)
- [Function Node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.function/)

### Инструменты:
- [JSONPath](https://jsonpath.com/) - работа с JSON
- [CSV Validator](https://csvlint.io/) - валидация CSV
- [Data Wrangler](https://github.com/microsoft/vscode-data-wrangler) - анализ данных

## Примеры обработки

### Валидация email:
```javascript
// Code Node
const email = $input.first().json.email;
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

if (!emailRegex.test(email)) {
  throw new Error('Invalid email format');
}

return { valid: true, email: email };
```

### Трансформация данных:
```javascript
// Function Node
const items = $input.all();
const transformed = items.map(item => ({
  id: item.json.id,
  name: item.json.name.toUpperCase(),
  created_at: new Date(item.json.timestamp).toISOString()
}));

return transformed;
```

### Обработка CSV:
```javascript
// Code Node
const csvData = $input.first().binary.data;
const text = Buffer.from(csvData, 'base64').toString('utf-8');
const lines = text.split('\n');
const headers = lines[0].split(',');

const result = lines.slice(1).map(line => {
  const values = line.split(',');
  const obj = {};
  headers.forEach((header, index) => {
    obj[header.trim()] = values[index]?.trim();
  });
  return obj;
});

return result;
```

---
*Последнее обновление: $(date)*

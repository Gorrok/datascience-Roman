# Templates - Готовые шаблоны процессов

## Описание
Папка содержит переиспользуемые шаблоны и базовые структуры для быстрого создания процессов.

## Путь
`./templates/`

## Категории шаблонов

### 📁 [basic/](./basic/)
- **Описание**: Базовые шаблоны для начинающих
- **Сложность**: Простые (1-3 узла)
- **Примеры**: Простые уведомления, базовые HTTP запросы

### 📁 [intermediate/](./intermediate/)
- **Описание**: Шаблоны средней сложности
- **Сложность**: Средние (4-10 узлов)
- **Примеры**: Обработка данных, интеграции

### 📁 [advanced/](./advanced/)
- **Описание**: Сложные шаблоны
- **Сложность**: Продвинутые (10+ узлов)
- **Примеры**: ETL процессы, сложные интеграции

### 📁 [node_examples/](./node_examples/)
- **Описание**: Примеры использования отдельных узлов
- **Функции**: Демонстрация возможностей узлов
- **Примеры**: HTTP Request, Code, Function

### 📁 [error_handling/](./error_handling/)
- **Описание**: Шаблоны обработки ошибок
- **Функции**: Retry логика, уведомления об ошибках
- **Примеры**: Try-catch блоки, fallback сценарии

## Типы шаблонов

### 🔄 Простые процессы
- **Webhook → HTTP Request → Response**
- **Schedule → Email → Log**
- **File Trigger → Process → Save**

### 🔄 Процессы с условиями
- **Trigger → IF → Action A / Action B**
- **Data → Switch → Multiple Actions**
- **Error → Retry → Fallback**

### 🔄 Циклические процессы
- **Loop → Process Item → Next**
- **Batch → Process Batch → Continue**
- **Queue → Process → Complete**

## Структура шаблона

### Обязательные элементы:
```json
{
  "template": {
    "name": "Template Name",
    "description": "Описание шаблона",
    "version": "1.0.0",
    "author": "Author Name",
    "tags": ["tag1", "tag2"],
    "nodes": [...],
    "connections": {...}
  }
}
```

### Дополнительные элементы:
- **README.md** - описание шаблона
- **config.json** - конфигурация
- **examples/** - примеры использования
- **tests/** - тестовые данные

## Лучшие практики создания шаблонов

### 1. Документация
- Подробное описание назначения
- Инструкции по настройке
- Примеры входных/выходных данных

### 2. Настройка
- Используйте переменные окружения
- Минимизируйте жестко заданные значения
- Предоставляйте примеры конфигурации

### 3. Тестирование
- Включайте тестовые данные
- Проверяйте все ветки выполнения
- Документируйте известные ограничения

### 4. Версионирование
- Используйте семантическое версионирование
- Ведите changelog
- Обеспечивайте обратную совместимость

## Частые ошибки в шаблонах

### ❌ Отсутствие документации
- **Проблема**: Непонятно как использовать шаблон
- **Решение**: Всегда включайте README и комментарии

### ❌ Жестко заданные значения
- **Проблема**: Шаблон не переиспользуется
- **Решение**: Используйте переменные и параметры

### ❌ Отсутствие обработки ошибок
- **Проблема**: Шаблон падает при ошибках
- **Решение**: Включайте базовую обработку ошибок

### ❌ Неоптимизированная структура
- **Проблема**: Слишком много узлов для простых задач
- **Решение**: Упрощайте и оптимизируйте

## Полезные ресурсы

### Официальные шаблоны:
- [n8n Workflow Templates](https://n8nworkflow.net/)
- [n8n Community Templates](https://community.n8n.io/c/workflows/5)
- [GitHub Templates](https://github.com/EugeneSadness/n8n-workflow-templates)

### Инструменты:
- [n8n Workflow Designer](https://n8n.io/workflow-designer/)
- [JSON Validator](https://jsonlint.com/)
- [Cron Expression Generator](https://crontab.guru/)

## Примеры шаблонов

### Базовый webhook:
```json
{
  "name": "Basic Webhook",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "webhook",
        "httpMethod": "POST"
      }
    },
    {
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ { \"status\": \"success\", \"data\": $json } }}"
      }
    }
  ],
  "connections": {
    "Webhook": {
      "main": [["Respond to Webhook"]]
    }
  }
}
```

### Обработка ошибок:
```json
{
  "name": "Error Handling Template",
  "nodes": [
    {
      "name": "Try Action",
      "type": "n8n-nodes-base.httpRequest"
    },
    {
      "name": "On Error",
      "type": "n8n-nodes-base.errorTrigger"
    },
    {
      "name": "Send Error Notification",
      "type": "n8n-nodes-base.emailSend"
    }
  ]
}
```

---
*Последнее обновление: $(date)*

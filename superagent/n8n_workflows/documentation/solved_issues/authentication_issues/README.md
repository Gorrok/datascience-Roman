# Authentication Issues - Проблемы аутентификации

## Описание
Решенные задачи связанные с аутентификацией, авторизацией и управлением доступом в n8n.

## Путь
`./documentation/solved_issues/authentication_issues/`

## Решенные задачи

### ISSUE-001: OAuth токен истекает и не обновляется автоматически

#### Проблема
OAuth токен истекает через определенное время, и процесс падает с ошибкой 401 Unauthorized.

#### Симптомы
- Процесс работает некоторое время, затем падает
- Ошибка 401 Unauthorized
- Сообщение "Token expired" в логах

#### Ошибки
```
HTTP 401 Unauthorized
{
  "error": "invalid_token",
  "error_description": "The access token expired"
}
```

#### Причина
OAuth токен имеет ограниченное время жизни и не обновляется автоматически.

#### Решение
1. Настройте автоматическое обновление токена в credentials
2. Используйте refresh token для получения нового access token
3. Добавьте обработку ошибки 401 с повторной аутентификацией

#### Код решения
```javascript
// Проверка и обновление токена
const checkToken = async () => {
  try {
    const response = await $http.request({
      url: 'https://api.example.com/user',
      headers: {
        'Authorization': `Bearer ${$credentials.accessToken}`
      }
    });
    return response;
  } catch (error) {
    if (error.status === 401) {
      // Обновляем токен
      const newToken = await refreshAccessToken();
      $credentials.accessToken = newToken;
      // Повторяем запрос
      return await $http.request({
        url: 'https://api.example.com/user',
        headers: {
          'Authorization': `Bearer ${newToken}`
        }
      });
    }
    throw error;
  }
};

const refreshAccessToken = async () => {
  const response = await $http.request({
    url: 'https://api.example.com/oauth/token',
    method: 'POST',
    body: {
      grant_type: 'refresh_token',
      refresh_token: $credentials.refreshToken,
      client_id: $credentials.clientId,
      client_secret: $credentials.clientSecret
    }
  });
  return response.access_token;
};
```

#### Профилактика
- Настройте автоматическое обновление токенов
- Используйте refresh token
- Добавьте обработку ошибок аутентификации

#### Связанные задачи
- ISSUE-002: API ключ не работает
- ISSUE-003: Неправильные credentials

#### Теги
`oauth`, `token`, `authentication`, `401`, `refresh`

#### Дата решения
2024-01-15

#### Автор решения
n8n Agent

---

### ISSUE-002: API ключ не работает после обновления

#### Проблема
API ключ перестал работать после обновления в внешнем сервисе.

#### Симптомы
- Ошибка 403 Forbidden
- Сообщение "Invalid API key"
- Процесс не может подключиться к API

#### Ошибки
```
HTTP 403 Forbidden
{
  "error": "invalid_api_key",
  "message": "The provided API key is invalid"
}
```

#### Причина
API ключ был обновлен в внешнем сервисе, но не обновлен в n8n credentials.

#### Решение
1. Проверьте актуальность API ключа в внешнем сервисе
2. Обновите API ключ в n8n credentials
3. Протестируйте подключение

#### Код решения
```javascript
// Проверка API ключа
const testApiKey = async () => {
  try {
    const response = await $http.request({
      url: 'https://api.example.com/test',
      headers: {
        'X-API-Key': $credentials.apiKey
      }
    });
    return { valid: true, response };
  } catch (error) {
    if (error.status === 403) {
      throw new Error('API key is invalid. Please update credentials.');
    }
    throw error;
  }
};
```

#### Профилактика
- Регулярно проверяйте актуальность API ключей
- Используйте тестовые endpoints для проверки
- Настройте уведомления об истечении ключей

#### Связанные задачи
- ISSUE-001: OAuth токен истекает
- ISSUE-004: Неправильные права доступа

#### Теги
`api_key`, `credentials`, `403`, `forbidden`

#### Дата решения
2024-01-16

#### Автор решения
n8n Agent

---

## Статистика категории

### Всего решенных задач: 2
### Последнее обновление: 2024-01-16

## Полезные ресурсы

### Документация:
- [n8n Credentials](https://docs.n8n.io/integrations/credentials/)
- [OAuth2 Authentication](https://docs.n8n.io/integrations/credentials/oauth2/)

### Инструменты:
- [OAuth 2.0 Playground](https://oauth2.thephpleague.com/)
- [JWT Debugger](https://jwt.io/)

---
*Категория постоянно обновляется новыми решениями*
*Последнее обновление: $(date)*

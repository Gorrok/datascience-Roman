# Реализация анализа изображений через OpenAI Assistant в n8n

Этот документ описывает шаги по созданию рабочего процесса (workflow) в n8n для анализа изображений с использованием OpenAI Assistants API. Этот подход позволяет создать более сложного и управляемого "агента" по сравнению с прямыми вызовами API.

## Преимущества OpenAI Assistants API

- **Постоянные инструкции**: Вы можете задать ассистенту определенную роль и инструкции (промпт), которые он будет постоянно использовать.
- **Состояние диалога (Threads)**: Ассистент "помнит" предыдущие сообщения в рамках одного диалога, что позволяет вести контекстуальные беседы.
- **Работа с файлами**: Ассистент может работать с файлами, включая изображения.

## Шаги по реализации в n8n

Процесс будет состоять из нескольких шагов, каждый из которых реализуется через ноду `HTTP Request` в n8n.

**Почему не использовать встроенную ноду OpenAI?**

На данный момент встроенная нода `OpenAI` в n8n (в режиме `Assistant -> Message an Assistant`) не имеет в интерфейсе функции для прикрепления изображений к сообщению. Она отлично подходит для текстовых чатов, но для анализа изображений потребуется "ручная" сборка запроса через ноду `HTTP Request`, как описано ниже.

### Шаг 1: Создание Ассистента (однократно)

Этого ассистента нужно создать один раз. Вы можете сделать это либо через [панель OpenAI](https://platform.openai.com/assistants), либо через API. При создании вы укажете ему инструкции (ваш промпт) и выберете модель.

- **Модель**: Используйте `gpt-4-turbo` или `gpt-4o`, так как они поддерживают анализ изображений.
- **Instructions**: Здесь вы указываете ваш подготовленный промпт. Например: "Ты — ассистент по анализу фотографий. Проанализируй изображение и верни данные в формате JSON со следующими полями: `description`, `objects_detected`, `dominant_colors`."

**Важно**: После создания сохраните `assistant_id`. Он понадобится вам в n8n.

### Шаг 2: Настройка Workflow в n8n

Ниже представлена последовательность нод для вашего workflow.

#### 1. Start / Webhook

Ваш workflow должен начинаться с триггера. Это может быть `Start` (для ручного запуска), `Webhook` (если вы отправляете картинку из другого сервиса) или любой другой триггер, который предоставляет изображение.

#### 2. HTTP Request: Создание диалога (Create Thread)

Каждый новый анализ изображения лучше начинать в новом "диалоге" (Thread).

- **Method**: `POST`
- **URL**: `https://api.openai.com/v1/threads`
- **Authentication**: `Header Auth`
- **Name**: `Authorization`
- **Value**: `Bearer YOUR_OPENAI_API_KEY`
- **Headers**:
    - `OpenAI-Beta`: `assistants=v2`

Эта нода создаст пустой диалог и вернет его ID (`id`).

#### 3. HTTP Request: Добавление сообщения с картинкой (Add Message)

Теперь добавим в созданный диалог сообщение, содержащее и текстовый запрос, и изображение.

- **Method**: `POST`
- **URL**: `https://api.openai.com/v1/threads/{{$node["Create Thread"].json.id}}/messages` (используем ID из предыдущей ноды)
- **Authentication**: `Header Auth` (аналогично предыдущему шагу)
- **Headers**:
    - `OpenAI-Beta`: `assistants=v2`
- **Body Content Type**: `JSON`
- **JSON Parameters**:
    - **role**: `user`
    - **content[0][type]**: `text`
    - **content[0][text]**: `Проанализируй это изображение.` (или любой другой ваш запрос)
    - **content[1][type]**: `image_url`
    - **content[1][image_url][url]**: `{{ $json.imageUrl }}` (здесь должна быть переменная, содержащая URL изображения, которая пришла из стартовой ноды. Если у вас бинарные данные, их нужно сначала куда-то загрузить, чтобы получить URL, или передать как file).

#### 4. HTTP Request: Запуск Ассистента (Create Run)

Эта нода запускает обработку диалога вашим ассистентом.

- **Method**: `POST`
- **URL**: `https://api.openai.com/v1/threads/{{$node["Create Thread"].json.id}}/runs`
- **Authentication**: `Header Auth`
- **Headers**:
    - `OpenAI-Beta`: `assistants=v2`

Этот подход, хотя и требует больше шагов, чем простой вызов API, предоставляет гораздо больше гибкости и контроля над процессом анализа, позволяя использовать все возможности OpenAI Assistants.

## Адаптация существующего Workflow (Ваш случай)

Если у вас уже есть workflow, который получает изображение (например, через `HTTP Request`), вот как заменить существующую ноду `OpenAI` на Assistant.

Предположим, ваша цепочка выглядит так:
`... -> HTTP Request (получает бинарные данные изображения) -> OpenAI Node -> ...`

Мы заменяем `OpenAI Node` на следующую последовательность:

### 1. HTTP Request: Загрузка изображения в OpenAI (Upload File)

Эта нода берет бинарные данные изображения из предыдущего шага и загружает их в OpenAI, чтобы получить `file_id`.

- **Method**: `POST`
- **URL**: `https://api.openai.com/v1/files`
- **Authentication**: `Header Auth`
- **Name**: `Authorization`
- **Value**: `Bearer YOUR_OPENAI_API_KEY`
- **Send Body**: `true`
- **Body Content Type**: `Form-Data Multipart`
- **Fields**:
    - **Add Field**:
        - **Name**: `purpose`
        - **Value**: `vision`
    - **Add Field**:
        - **Parameter Type**: `File`
        - **Name**: `file`
        - **Property Name**: `data` (имя свойства из предыдущей ноды, где хранятся бинарные данные файла)

**Результат**: Эта нода вернет JSON с `id` файла (например, `file-xxxxxxxx`).

### 2. HTTP Request: Создание диалога (Create Thread)

Этот шаг остается таким же, как в основной инструкции (делает `POST` на `https://api.openai.com/v1/threads`).

### 3. HTTP Request: Добавление сообщения с файлом (Add Message)

Теперь мы добавляем сообщение в диалог, используя `file_id` из шага 1.

- **Method**: `POST`
- **URL**: `https://api.openai.com/v1/threads/{{$node["Create Thread"].json.id}}/messages`
- **Authentication**: `Header Auth`
- **Headers**: `OpenAI-Beta: assistants=v2`
- **Body Content Type**: `JSON`
- **JSON Parameters**:
    - **role**: `user`
    - **content[0][type]**: `text`
    - **content[0][text]**: `Проанализируй это изображение согласно моим инструкциям.`
    - **content[1][type]**: `image_file`
    - **content[1][image_file][file_id]**: `{{$node["Upload File"].json.id}}` (ID из ноды загрузки файла)

### 4. Последующие шаги (Run, Wait, Check Status, Get Response)

Все последующие шаги (`Create Run`, `Wait`, `Retrieve Run`, `List Messages`) остаются такими же, как описано в основной инструкции выше. Вы просто строите эту цепочку нод вместо вашей одной ноды `OpenAI`.
# Profit Premium — Рабочий журнал

> Этот файл обновляется после каждой сессии. Здесь хранится весь контекст по проекту.

**Репозиторий**: https://github.com/LionMux/Profit-Premium  
**Форк (для PR)**: https://github.com/Gorrok/Profit-Premium  
**Последнее обновление**: 2026-04-08

---

## О проекте

**Profit Premium** — двухуровневый сайт агентства недвижимости:

| Уровень | URL | Описание |
|---|---|---|
| Публичный лендинг | `/` | Для клиентов агентства |
| Личный кабинет | `/login` → `/cabinet` | Для агентов-партнёров |

---

## Стек технологий

| Компонент | Технология |
|---|---|
| Framework | Next.js 14 (App Router) |
| Language | TypeScript 5.x |
| Styling | Tailwind CSS 3.x |
| UI Kit | shadcn/ui (Radix UI) |
| Fonts | Inter (body) + Cormorant Garamond (headings) |
| ORM | Prisma 5.x |
| Database | PostgreSQL 15+ |
| Auth | NextAuth.js 5.x |
| SMS | SMS.ru API |
| CRM | Bitrix24 Webhook |
| Testing | Playwright (E2E) |
| CI/CD | GitHub Actions |
| Deploy | Docker + VPS |

---

## Дизайн-система

### Цвета (лендинг)
```
Бордо основной:  #5C1E2D  (burgundy)
Бордо тёмный:   #3D1220  (burgundy-dark)
Бордо средний:  #7A2B3E  (burgundy-medium)
Кремовый:       #F0EAE0  (cream)
Кремовый тёмный: #E0D5C5 (cream-dark)
Кремовый светлый: #F8F4EF (cream-light)
```

### Типографика
- Заголовки: `font-serif` (Cormorant Garamond), UPPERCASE
- Текст: `font-sans` (Inter)
- Метки/кнопки: `tracking-[0.2em]` или `tracking-[0.3em]`, `text-xs`, `font-bold`

### Компоненты лендинга
```
src/components/landing/
├── Sidebar.tsx       — правый фиксированный сайдбар + мобильный бургер
├── HeroSection.tsx   — первый экран, бордо фон
├── AdvantagesSection.tsx — 4 карточки преимуществ, кремовый фон
├── ServicesSection.tsx   — 4 услуги, бордо фон
├── TeamSection.tsx       — команда, светло-кремовый фон
├── ReviewsSection.tsx    — отзывы, тёмный бордо фон
└── ContactSection.tsx    — форма + footer
```

---

## История PR

| PR | Ветка | Статус | Описание |
|---|---|---|---|
| [#1](https://github.com/LionMux/Profit-Premium/pull/1) | `feat/public-landing-page` | ✅ Merged | Каркас лендинга (6 секций) + фикс CI |
| [#2](https://github.com/LionMux/Profit-Premium/pull/2) | `feat/landing-brand-redesign` | 🔄 Open | Редизайн под бренд PROFIT PREMIUM |

---

## Рабочий процесс (как делать PR)

### 1. Клонировать и настроить
```bash
cd /tmp
git clone https://github.com/LionMux/Profit-Premium.git profit-premium
cd profit-premium
git remote add fork https://Gorrok:<TOKEN>@github.com/Gorrok/Profit-Premium.git
```

### 2. Создать ветку от актуального main
```bash
git fetch origin
git checkout -b feat/название-фичи origin/main
```

### 3. Внести изменения, затем ОБЯЗАТЕЛЬНО перед коммитом
```bash
npm install          # нужен для prettier
npx prettier --write .  --ignore-path .gitignore
```

### 4. Коммит и пуш
```bash
git add -A
git commit -m "feat(scope): описание"
git push fork feat/название-фичи
```

### 5. Создать PR через API
```bash
curl -X POST \
  -H "Authorization: token <TOKEN>" \
  -H "Accept: application/vnd.github+json" \
  https://api.github.com/repos/LionMux/Profit-Premium/pulls \
  -d '{"title":"...","head":"Gorrok:ветка","base":"main","body":"..."}'
```

---

## Типичные ошибки CI и как избегать

### ❌ Ошибка 1: `npm ci` падает — нет `package-lock.json`
**Причина**: в репо нет lock-файла, а `npm ci` его требует.  
**Решение**: CI использует `npm install` (уже исправлено в `.github/workflows/ci.yml`).  
**Правило**: не возвращать `npm ci` обратно.

### ❌ Ошибка 2: `Check formatting` падает — Prettier
**Причина**: код написан не по правилам `.prettierrc`.  
**Конфиг Prettier**:
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "arrowParens": "avoid"
}
```
**Решение**: всегда запускать `npx prettier --write .` перед коммитом.  
**Правило**: форматировать ВСЕ файлы, не только новые.

### ❌ Ошибка 3: `cache: 'npm'` в CI без lock-файла
**Причина**: `actions/setup-node@v4` с `cache: 'npm'` ищет `package-lock.json`.  
**Решение**: убрать `cache: 'npm'` из CI (уже исправлено).

### ❌ Ошибка 4: `action_required` — GitHub блокирует CI от форка
**Причина**: GitHub требует одобрение для форков (безопасность).  
**Решение**: Settings → Actions → General → изменить на "first-time contributors only".  
**Статус**: ✅ уже настроено.

---

## Текущее состояние `main`

### Что есть на main (после мержа PR #1):
- ✅ Публичный лендинг (6 секций, старый дизайн slate+amber)
- ✅ Исправленный CI (npm install вместо npm ci)
- ✅ Prettier отформатированы все файлы
- ✅ Заготовки всех страниц личного кабинета (пустые)
- ✅ Prisma schema + seed
- ✅ API роуты (заготовки)
- ✅ Компоненты auth, layout (заготовки)

### Что в PR #2 (ожидает merge):
- 🔄 Полный редизайн под бренд PROFIT PREMIUM
- 🔄 Правый сайдбар вместо top navbar
- 🔄 Цвета бордо + крем
- 🔄 Шрифт Cormorant Garamond
- 🔄 Tailwind: новые цвета burgundy/cream

---

## Что нужно сделать (бэклог)

### Лендинг
- [ ] Заменить заглушки на реальные данные (контакты, команда, отзывы)
- [ ] Подключить форму заявки к реальному API / email
- [ ] Добавить анимации при скролле
- [ ] SEO мета-теги

### Личный кабинет (отдельная задача)
- [ ] Страница логина (email + SMS)
- [ ] Главная с каруселью сторис
- [ ] Страница материалов с фильтрами
- [ ] Профиль + форма передачи клиента → Bitrix24
- [ ] Страница контактов (юр. информация)
- [ ] Админ-панель (загрузка материалов)

### Инфраструктура
- [ ] База данных (PostgreSQL + Prisma migrate)
- [ ] Настройка .env для продакшена
- [ ] Docker deploy на VPS
- [ ] SMS.ru интеграция

---

## Тестовые данные (из AGENTS.md)

```
Admin:   admin@profit-premium.ru  / admin123
Partner: partner@example.com      / partner123
```

---

## Контакты проекта (заглушки, нужно уточнить)

```
Телефон:  +7 (000) 000-00-00
Email:    info@profit-premium.ru
Соцсети:  Telegram / WhatsApp / ВКонтакте (ссылки не указаны)
```

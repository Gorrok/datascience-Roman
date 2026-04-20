FROM node:20-alpine

WORKDIR /app

# Копируем package files
COPY package*.json ./

# Устанавливаем зависимости
RUN npm ci

# Копируем остальные файлы
COPY . .

# Экспортируем порт
EXPOSE 3000

# Запускаем dev сервер
CMD ["npm", "run", "dev"]

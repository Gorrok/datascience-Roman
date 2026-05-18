'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Hero Section */}
      <div className="container mx-auto px-6 pt-20 pb-32">
        <div className="text-center max-w-4xl mx-auto">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-6">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
            Запустите за 2 минуты
          </div>

          {/* Heading */}
          <h1 className="text-6xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-gray-900 via-blue-800 to-purple-900 bg-clip-text text-transparent leading-tight">
            Аналитика Telegram
            <br />
            каналов в 1 клик
          </h1>

          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto leading-relaxed">
            Добавьте бота, выберите канал — и всё. Никакой настройки. 
            Видите кто подписался, кто отписался, какие ссылки работают.
          </p>

          {/* CTA Buttons */}
          <div className="flex gap-4 justify-center items-center">
            <a href="/register">
              <Button size="lg" className="text-lg px-8 py-6 rounded-xl shadow-lg hover:shadow-xl transition-all">
                Начать бесплатно →
              </Button>
            </a>
            <a href="/dashboard">
              <Button size="lg" variant="outline" className="text-lg px-8 py-6 rounded-xl">
                Посмотреть демо
              </Button>
            </a>
          </div>

          <p className="text-sm text-gray-500 mt-6">
            14 дней бесплатно • Без карты • Отмена в 1 клик
          </p>
        </div>
      </div>

      {/* How it works */}
      <div className="container mx-auto px-6 pb-20">
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold mb-4">Как это работает</h2>
          <p className="text-gray-600 text-lg">Три простых шага до первой аналитики</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {/* Step 1 */}
          <Card className="p-8 border-2 hover:border-blue-500 transition-all hover:shadow-lg">
            <div className="text-5xl mb-6">🤖</div>
            <div className="text-sm text-blue-600 font-semibold mb-2">ШАГ 1</div>
            <h3 className="text-2xl font-bold mb-4">Добавьте бота</h3>
            <p className="text-gray-600 leading-relaxed">
              Создайте бота через @BotFather, вставьте токен — готово.
              Занимает 30 секунд.
            </p>
          </Card>

          {/* Step 2 */}
          <Card className="p-8 border-2 hover:border-purple-500 transition-all hover:shadow-lg">
            <div className="text-5xl mb-6">📱</div>
            <div className="text-sm text-purple-600 font-semibold mb-2">ШАГ 2</div>
            <h3 className="text-2xl font-bold mb-4">Выберите канал</h3>
            <p className="text-gray-600 leading-relaxed">
              Бот покажет все ваши каналы. Кликните на нужный — 
              мониторинг начнётся автоматически.
            </p>
          </Card>

          {/* Step 3 */}
          <Card className="p-8 border-2 hover:border-green-500 transition-all hover:shadow-lg">
            <div className="text-5xl mb-6">📊</div>
            <div className="text-sm text-green-600 font-semibold mb-2">ШАГ 3</div>
            <h3 className="text-2xl font-bold mb-4">Смотрите данные</h3>
            <p className="text-gray-600 leading-relaxed">
              Сразу видите: кто подписался, кто ушёл, эффективность 
              каждой инвайт-ссылки. Красиво и понятно.
            </p>
          </Card>
        </div>
      </div>

      {/* Features */}
      <div className="bg-gray-50 py-20">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Всё что нужно, ничего лишнего</h2>
          </div>

          <div className="grid md:grid-cols-2 gap-6 max-w-5xl mx-auto">
            <Card className="p-6 flex gap-4 items-start hover:shadow-md transition-shadow">
              <div className="text-3xl">📈</div>
              <div>
                <h3 className="font-semibold text-lg mb-2">Графики роста</h3>
                <p className="text-gray-600">Видите динамику подписок/отписок по дням</p>
              </div>
            </Card>

            <Card className="p-6 flex gap-4 items-start hover:shadow-md transition-shadow">
              <div className="text-3xl">🔗</div>
              <div>
                <h3 className="font-semibold text-lg mb-2">Топ инвайт-ссылок</h3>
                <p className="text-gray-600">Какие ссылки приводят больше подписчиков</p>
              </div>
            </Card>

            <Card className="p-6 flex gap-4 items-start hover:shadow-md transition-shadow">
              <div className="text-3xl">📑</div>
              <div>
                <h3 className="font-semibold text-lg mb-2">Экспорт в Sheets</h3>
                <p className="text-gray-600">Выгружайте данные в Google таблицы автоматически</p>
              </div>
            </Card>

            <Card className="p-6 flex gap-4 items-start hover:shadow-md transition-shadow">
              <div className="text-3xl">⚡</div>
              <div>
                <h3 className="font-semibold text-lg mb-2">Реальное время</h3>
                <p className="text-gray-600">Данные обновляются моментально</p>
              </div>
            </Card>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="container mx-auto px-6 py-20 text-center">
        <h2 className="text-4xl font-bold mb-6">Попробуйте прямо сейчас</h2>
        <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          Первые 14 дней бесплатно. Без карты. Отмена в любой момент.
        </p>
        <a href="/register">
          <Button size="lg" className="text-lg px-12 py-6 rounded-xl shadow-lg hover:shadow-xl">
            Начать за 30 секунд →
          </Button>
        </a>
      </div>
    </main>
  );
}

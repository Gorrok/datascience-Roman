'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { botsApi } from '@/lib/api';

export default function BotsPage() {
  const router = useRouter();
  const [bots, setBots] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [botToken, setBotToken] = useState('');
  const [botName, setBotName] = useState('');
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadBots();
  }, []);

  const loadBots = async () => {
    try {
      setLoading(true);
      const response = await botsApi.getAll();
      setBots(response.data);
    } catch (error) {
      console.error('Error loading bots:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddBot = async (e: React.FormEvent) => {
    e.preventDefault();
    setAdding(true);
    setError('');

    try {
      await botsApi.create({ bot_token: botToken });
      await loadBots();
      setShowAddForm(false);
      setBotToken('');
      setBotName('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка добавления бота');
    } finally {
      setAdding(false);
    }
  };

  const handleStartBot = async (botId: number) => {
    try {
      await botsApi.start(botId);
      await loadBots();
    } catch (error) {
      console.error('Error starting bot:', error);
    }
  };

  const handleStopBot = async (botId: number) => {
    try {
      await botsApi.stop(botId);
      await loadBots();
    } catch (error) {
      console.error('Error stopping bot:', error);
    }
  };

  const handleDeleteBot = async (botId: number) => {
    if (!confirm('Удалить бота?')) return;

    try {
      await botsApi.delete(botId);
      await loadBots();
    } catch (error) {
      console.error('Error deleting bot:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="outline" onClick={() => router.push('/dashboard')}>
              ← Назад
            </Button>
            <h1 className="text-2xl font-bold">Управление ботами</h1>
          </div>
          <Button onClick={() => setShowAddForm(true)}>+ Добавить бота</Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        {/* Add Bot Form */}
        {showAddForm && (
          <Card className="mb-6 shadow-lg">
            <CardHeader>
              <CardTitle>Добавить нового бота</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleAddBot} className="space-y-4">
                {error && (
                  <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                <div>
                  <label className="block text-sm font-medium mb-2">Название бота</label>
                  <input
                    type="text"
                    value={botName}
                    onChange={(e) => setBotName(e.target.value)}
                    placeholder="Мой бот"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Токен бота</label>
                  <input
                    type="text"
                    value={botToken}
                    onChange={(e) => setBotToken(e.target.value)}
                    placeholder="123456:ABCdefGHIjklMNOpqrsTUVwxyz"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    required
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Получите токен у{' '}
                    <a href="https://t.me/botfather" target="_blank" className="text-blue-600 hover:underline">
                      @BotFather
                    </a>
                  </p>
                </div>

                <div className="flex gap-3">
                  <Button type="button" variant="outline" onClick={() => setShowAddForm(false)}>
                    Отмена
                  </Button>
                  <Button type="submit" disabled={adding}>
                    {adding ? 'Добавляем...' : 'Добавить бота'}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Bots List */}
        {loading ? (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">⏳</div>
            <p className="text-xl text-gray-600">Загружаем ботов...</p>
          </div>
        ) : bots.length === 0 ? (
          <Card className="text-center py-20">
            <CardContent>
              <div className="text-6xl mb-4">🤖</div>
              <h2 className="text-2xl font-bold mb-2">Нет ботов</h2>
              <p className="text-gray-600 mb-6">Добавьте вашего первого бота</p>
              <Button onClick={() => setShowAddForm(true)}>+ Добавить бота</Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6">
            {bots.map((bot) => (
              <Card key={bot.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <div className="text-4xl">🤖</div>
                        <div>
                          <h3 className="text-xl font-bold">{bot.name}</h3>
                          <p className="text-sm text-gray-600">@{bot.username}</p>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-4 mt-4">
                        <div>
                          <p className="text-sm text-gray-600">ID бота</p>
                          <p className="font-mono text-sm">{bot.bot_id}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Статус</p>
                          <span
                            className={`inline-block px-2 py-1 rounded text-xs font-semibold ${
                              bot.is_active
                                ? 'bg-green-100 text-green-700'
                                : 'bg-gray-100 text-gray-700'
                            }`}
                          >
                            {bot.is_active ? 'Активен' : 'Остановлен'}
                          </span>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Создан</p>
                          <p className="text-sm">{new Date(bot.created_at).toLocaleDateString('ru-RU')}</p>
                        </div>
                      </div>
                    </div>

                    <div className="flex flex-col gap-2 ml-4">
                      {bot.is_active ? (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleStopBot(bot.id)}
                          className="text-red-600 hover:bg-red-50"
                        >
                          Остановить
                        </Button>
                      ) : (
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleStartBot(bot.id)}
                          className="text-green-600 hover:bg-green-50"
                        >
                          Запустить
                        </Button>
                      )}
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDeleteBot(bot.id)}
                        className="text-red-600 hover:bg-red-50"
                      >
                        Удалить
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { botsApi, channelsApi } from '@/lib/api';

export default function ChannelsPage() {
  const router = useRouter();
  const [bots, setBots] = useState<any[]>([]);
  const [selectedBotId, setSelectedBotId] = useState<number | null>(null);
  const [channels, setChannels] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [channelId, setChannelId] = useState('');
  const [channelName, setChannelName] = useState('');
  const [adding, setAdding] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadBots();
  }, []);

  useEffect(() => {
    if (selectedBotId) {
      loadChannels(selectedBotId);
    }
  }, [selectedBotId]);

  const loadBots = async () => {
    try {
      const response = await botsApi.getAll();
      setBots(response.data);
      if (response.data.length > 0) {
        setSelectedBotId(response.data[0].id);
      }
      setLoading(false);
    } catch (error) {
      console.error('Error loading bots:', error);
      setLoading(false);
    }
  };

  const loadChannels = async (botId: number) => {
    try {
      const response = await channelsApi.getAll(botId);
      setChannels(response.data);
    } catch (error) {
      console.error('Error loading channels:', error);
    }
  };

  const handleAddChannel = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedBotId) return;

    setAdding(true);
    setError('');

    try {
      await channelsApi.create(selectedBotId, {
        telegram_channel_id: parseInt(channelId),
        channel_title: channelName,
      });
      await loadChannels(selectedBotId);
      setShowAddForm(false);
      setChannelId('');
      setChannelName('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка добавления канала');
    } finally {
      setAdding(false);
    }
  };

  const handleDeleteChannel = async (channelId: number) => {
    if (!confirm('Удалить канал?')) return;

    try {
      await channelsApi.delete(channelId);
      if (selectedBotId) {
        await loadChannels(selectedBotId);
      }
    } catch (error) {
      console.error('Error deleting channel:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">⏳</div>
          <p className="text-xl text-gray-600">Загружаем данные...</p>
        </div>
      </div>
    );
  }

  if (bots.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white border-b">
          <div className="container mx-auto px-6 py-4 flex items-center gap-4">
            <Button variant="outline" onClick={() => router.push('/dashboard')}>
              ← Назад
            </Button>
            <h1 className="text-2xl font-bold">Управление каналами</h1>
          </div>
        </div>

        <div className="flex items-center justify-center px-4 py-20">
          <Card className="max-w-xl w-full shadow-xl">
            <CardContent className="text-center py-12">
              <div className="text-6xl mb-4">🤖</div>
              <h2 className="text-2xl font-bold mb-2">Сначала добавьте бота</h2>
              <p className="text-gray-600 mb-6">У вас нет ботов для управления каналами</p>
              <Button onClick={() => router.push('/bots')}>Перейти к ботам →</Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="outline" onClick={() => router.push('/dashboard')}>
              ← Назад
            </Button>
            <h1 className="text-2xl font-bold">Управление каналами</h1>
          </div>
          <Button onClick={() => setShowAddForm(true)}>+ Добавить канал</Button>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        {/* Bot Selector */}
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">Выберите бота</label>
          <select
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            value={selectedBotId || ''}
            onChange={(e) => setSelectedBotId(parseInt(e.target.value))}
          >
            {bots.map((bot) => (
              <option key={bot.id} value={bot.id}>
                {bot.name} (@{bot.username})
              </option>
            ))}
          </select>
        </div>

        {/* Add Channel Form */}
        {showAddForm && (
          <Card className="mb-6 shadow-lg">
            <CardHeader>
              <CardTitle>Добавить новый канал</CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleAddChannel} className="space-y-4">
                {error && (
                  <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm text-gray-700">
                    <strong>Как получить ID канала:</strong>
                  </p>
                  <ol className="text-sm text-gray-600 mt-2 space-y-1 ml-4 list-decimal">
                    <li>Добавьте бота в канал как администратора</li>
                    <li>
                      Отправьте любое сообщение в канал и перешлите его{' '}
                      <a
                        href="https://t.me/username_to_id_bot"
                        target="_blank"
                        className="text-blue-600 hover:underline"
                      >
                        @username_to_id_bot
                      </a>
                    </li>
                    <li>Бот пришлёт вам ID канала (например: -1001234567890)</li>
                  </ol>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Название канала</label>
                  <input
                    type="text"
                    value={channelName}
                    onChange={(e) => setChannelName(e.target.value)}
                    placeholder="Мой канал"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">ID канала</label>
                  <input
                    type="text"
                    value={channelId}
                    onChange={(e) => setChannelId(e.target.value)}
                    placeholder="-1001234567890"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
                    required
                  />
                </div>

                <div className="flex gap-3">
                  <Button type="button" variant="outline" onClick={() => setShowAddForm(false)}>
                    Отмена
                  </Button>
                  <Button type="submit" disabled={adding}>
                    {adding ? 'Добавляем...' : 'Добавить канал'}
                  </Button>
                </div>
              </form>
            </CardContent>
          </Card>
        )}

        {/* Channels List */}
        {channels.length === 0 ? (
          <Card className="text-center py-20">
            <CardContent>
              <div className="text-6xl mb-4">📱</div>
              <h2 className="text-2xl font-bold mb-2">Нет каналов</h2>
              <p className="text-gray-600 mb-6">Добавьте канал для мониторинга</p>
              <Button onClick={() => setShowAddForm(true)}>+ Добавить канал</Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6">
            {channels.map((channel) => (
              <Card key={channel.id} className="hover:shadow-lg transition-shadow">
                <CardContent className="p-6">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3 mb-3">
                        <div className="text-4xl">📱</div>
                        <div>
                          <h3 className="text-xl font-bold">{channel.name}</h3>
                          <p className="text-sm text-gray-600">ID: {channel.telegram_id}</p>
                        </div>
                      </div>

                      <div className="grid grid-cols-3 gap-4 mt-4">
                        <div>
                          <p className="text-sm text-gray-600">Участников</p>
                          <p className="text-2xl font-bold">{channel.member_count || 0}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Активен с</p>
                          <p className="text-sm">{new Date(channel.created_at).toLocaleDateString('ru-RU')}</p>
                        </div>
                        <div>
                          <p className="text-sm text-gray-600">Статус</p>
                          <span className="inline-block px-2 py-1 rounded text-xs font-semibold bg-green-100 text-green-700">
                            Активен
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="flex flex-col gap-2 ml-4">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => router.push(`/dashboard?channel=${channel.id}`)}
                      >
                        Аналитика
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDeleteChannel(channel.id)}
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

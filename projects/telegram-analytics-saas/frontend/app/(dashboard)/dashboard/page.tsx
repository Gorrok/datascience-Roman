'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { botsApi, channelsApi, analyticsApi } from '@/lib/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';

export default function Dashboard() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);
  const [bots, setBots] = useState<any[]>([]);
  const [channels, setChannels] = useState<any[]>([]);
  const [selectedChannel, setSelectedChannel] = useState<any>(null);
  const [stats, setStats] = useState<any>(null);
  const [showAddBot, setShowAddBot] = useState(false);
  const [botToken, setBotToken] = useState('');
  const [addingBot, setAddingBot] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const botsResponse = await botsApi.getAll();
      setBots(botsResponse.data);

      if (botsResponse.data.length > 0) {
        const channelsResponse = await channelsApi.getAll(botsResponse.data[0].id);
        setChannels(channelsResponse.data);

        if (channelsResponse.data.length > 0) {
          setSelectedChannel(channelsResponse.data[0]);
          const statsResponse = await analyticsApi.getStats(channelsResponse.data[0].id);
          setStats(statsResponse.data);
        }
      }
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddBot = async (e: React.FormEvent) => {
    e.preventDefault();
    setAddingBot(true);
    setError('');

    try {
      await botsApi.create({ bot_token: botToken });
      await loadData();
      setShowAddBot(false);
      setBotToken('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка добавления бота');
    } finally {
      setAddingBot(false);
    }
  };

  // Онбординг: нет ботов
  if (!loading && bots.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        {/* Header */}
        <div className="bg-white border-b">
          <div className="container mx-auto px-6 py-4 flex items-center justify-between">
            <h1 className="text-2xl font-bold">Telegram Analytics</h1>
            <Button variant="outline" onClick={() => router.push('/settings')}>
              Настройки
            </Button>
          </div>
        </div>

        {/* Onboarding */}
        <div className="flex items-center justify-center px-4 py-20">
          <Card className="max-w-2xl w-full shadow-2xl border-0">
            <CardHeader className="text-center pb-8">
              <div className="text-6xl mb-4">🤖</div>
              <CardTitle className="text-3xl mb-2">Добавьте вашего первого бота</CardTitle>
              <p className="text-gray-600 text-lg">Это займёт всего 30 секунд</p>
            </CardHeader>
            <CardContent>
              {!showAddBot ? (
                <div className="space-y-6">
                  <div className="bg-blue-50 p-6 rounded-xl">
                    <h3 className="font-semibold mb-3 flex items-center gap-2">
                      <span className="bg-blue-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm">
                        1
                      </span>
                      Создайте бота в Telegram
                    </h3>
                    <p className="text-gray-600 mb-3">
                      Откройте{' '}
                      <a
                        href="https://t.me/botfather"
                        target="_blank"
                        className="text-blue-600 font-medium hover:underline"
                      >
                        @BotFather
                      </a>{' '}
                      и отправьте /newbot
                    </p>
                  </div>

                  <div className="bg-purple-50 p-6 rounded-xl">
                    <h3 className="font-semibold mb-3 flex items-center gap-2">
                      <span className="bg-purple-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm">
                        2
                      </span>
                      Скопируйте токен бота
                    </h3>
                    <p className="text-gray-600 mb-3">
                      @BotFather пришлёт вам токен вида:{' '}
                      <code className="bg-white px-2 py-1 rounded text-sm">123456:ABCdef...</code>
                    </p>
                  </div>

                  <div className="bg-green-50 p-6 rounded-xl">
                    <h3 className="font-semibold mb-3 flex items-center gap-2">
                      <span className="bg-green-500 text-white w-6 h-6 rounded-full flex items-center justify-center text-sm">
                        3
                      </span>
                      Вставьте токен
                    </h3>
                    <Button
                      className="w-full py-6 text-lg rounded-lg"
                      onClick={() => setShowAddBot(true)}
                    >
                      Добавить бота →
                    </Button>
                  </div>
                </div>
              ) : (
                <form onSubmit={handleAddBot} className="space-y-4">
                  {error && (
                    <div className="p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
                      {error}
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium mb-2">Токен бота</label>
                    <input
                      type="text"
                      value={botToken}
                      onChange={(e) => setBotToken(e.target.value)}
                      placeholder="123456:ABCdefGHIjklMNOpqrsTUVwxyz"
                      className="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition"
                      required
                    />
                  </div>

                  <div className="flex gap-3">
                    <Button
                      type="button"
                      variant="outline"
                      className="flex-1"
                      onClick={() => setShowAddBot(false)}
                    >
                      Назад
                    </Button>
                    <Button type="submit" className="flex-1" disabled={addingBot}>
                      {addingBot ? 'Добавляем...' : 'Добавить бота →'}
                    </Button>
                  </div>
                </form>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // Loading state
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

  // Есть боты, но нет каналов
  if (channels.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="bg-white border-b">
          <div className="container mx-auto px-6 py-4 flex items-center justify-between">
            <h1 className="text-2xl font-bold">Telegram Analytics</h1>
            <div className="flex gap-3">
              <Button variant="outline" onClick={() => router.push('/bots')}>
                Боты
              </Button>
              <Button variant="outline" onClick={() => router.push('/settings')}>
                Настройки
              </Button>
            </div>
          </div>
        </div>

        <div className="flex items-center justify-center px-4 py-20">
          <Card className="max-w-xl w-full shadow-xl">
            <CardHeader className="text-center">
              <div className="text-6xl mb-4">📱</div>
              <CardTitle className="text-2xl mb-2">Добавьте канал для мониторинга</CardTitle>
              <p className="text-gray-600">Перейдите на страницу управления каналами</p>
            </CardHeader>
            <CardContent>
              <Button className="w-full py-6 text-lg" onClick={() => router.push('/channels')}>
                Перейти к каналам →
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    );
  }

  // Главный дашборд
  const mockGrowthData = [
    { date: '1 мар', members: 1200 },
    { date: '2 мар', members: 1250 },
    { date: '3 мар', members: 1300 },
    { date: '4 мар', members: stats?.total_members || 1350 },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="text-2xl font-bold">Telegram Analytics</h1>
          <div className="flex gap-3">
            <Button variant="outline" onClick={() => router.push('/bots')}>
              Боты
            </Button>
            <Button variant="outline" onClick={() => router.push('/channels')}>
              Каналы
            </Button>
            <Button variant="outline" onClick={() => router.push('/settings')}>
              Настройки
            </Button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8">
        {/* Channel Selector */}
        <div className="mb-6">
          <label className="block text-sm font-medium mb-2">Выбранный канал</label>
          <select
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
            value={selectedChannel?.id}
            onChange={(e) => {
              const channel = channels.find((c) => c.id === parseInt(e.target.value));
              setSelectedChannel(channel);
            }}
          >
            {channels.map((channel) => (
              <option key={channel.id} value={channel.id}>
                {channel.name}
              </option>
            ))}
          </select>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <p className="text-sm text-gray-600 mb-1">Всего участников</p>
              <p className="text-4xl font-bold">{stats?.total_members || 0}</p>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <p className="text-sm text-gray-600 mb-1">Активных</p>
              <p className="text-4xl font-bold text-green-600">{stats?.active_members || 0}</p>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <p className="text-sm text-gray-600 mb-1">Новых сегодня</p>
              <p className="text-4xl font-bold text-blue-600">+{stats?.new_members || 0}</p>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardContent className="p-6">
              <p className="text-sm text-gray-600 mb-1">Ушло сегодня</p>
              <p className="text-4xl font-bold text-red-600">-{stats?.left_members || 0}</p>
            </CardContent>
          </Card>
        </div>

        {/* Charts */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle>График роста</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={mockGrowthData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="members" stroke="#3B82F6" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Топ инвайт-ссылок</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {stats?.top_invite_links?.length > 0 ? (
                  stats.top_invite_links.map((link: any, idx: number) => (
                    <div
                      key={idx}
                      className="flex items-center justify-between p-4 bg-blue-50 rounded-lg"
                    >
                      <div>
                        <p className="font-semibold">{link.name || 'Ссылка #' + (idx + 1)}</p>
                        <p className="text-sm text-gray-600">{link.count} подписчиков</p>
                      </div>
                      <div className="text-2xl font-bold text-blue-600">
                        {Math.round((link.count / stats.total_members) * 100)}%
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-gray-500">
                    Нет данных по инвайт-ссылкам
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

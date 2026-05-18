'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { authApi } from '@/lib/api';

export default function SettingsPage() {
  const router = useRouter();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const response = await authApi.getMe();
      setUser(response.data);
    } catch (error) {
      console.error('Error loading user:', error);
      router.push('/auth/login');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    router.push('/auth/login');
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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-6 py-4 flex items-center gap-4">
          <Button variant="outline" onClick={() => router.push('/dashboard')}>
            ← Назад
          </Button>
          <h1 className="text-2xl font-bold">Настройки</h1>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-6 py-8 max-w-4xl">
        {/* Profile */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Профиль</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Имя</label>
                <p className="text-lg">{user?.full_name}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Email</label>
                <p className="text-lg">{user?.email}</p>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Зарегистрирован
                </label>
                <p className="text-lg">{new Date(user?.created_at).toLocaleDateString('ru-RU')}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Subscription */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Подписка</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Тарифный план</label>
                <div className="flex items-center gap-3">
                  <span className="text-lg font-semibold">
                    {user?.subscription?.plan_type === 'trial' && '🆓 Пробный'}
                    {user?.subscription?.plan_type === 'basic' && '⭐ Базовый'}
                    {user?.subscription?.plan_type === 'pro' && '💎 Профессиональный'}
                    {user?.subscription?.plan_type === 'enterprise' && '🚀 Корпоративный'}
                  </span>
                  {user?.subscription?.is_active ? (
                    <span className="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">
                      Активна
                    </span>
                  ) : (
                    <span className="px-2 py-1 bg-red-100 text-red-700 text-xs rounded">
                      Неактивна
                    </span>
                  )}
                </div>
              </div>

              {user?.subscription?.trial_ends_at && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Пробный период до
                  </label>
                  <p className="text-lg">
                    {new Date(user.subscription.trial_ends_at).toLocaleDateString('ru-RU')}
                  </p>
                </div>
              )}

              <div className="pt-4">
                <Button variant="outline">Управление подпиской →</Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Limits */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle>Лимиты</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium">Боты</p>
                  <p className="text-sm text-gray-600">Максимальное количество ботов</p>
                </div>
                <p className="text-2xl font-bold">{user?.subscription?.max_bots || 1}</p>
              </div>

              <div className="flex justify-between items-center">
                <div>
                  <p className="font-medium">Каналы</p>
                  <p className="text-sm text-gray-600">Максимальное количество каналов</p>
                </div>
                <p className="text-2xl font-bold">{user?.subscription?.max_channels || 3}</p>
              </div>

              <div className="pt-4 border-t">
                <p className="text-sm text-gray-600">
                  Для увеличения лимитов обновите тарифный план
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Danger Zone */}
        <Card className="border-red-200">
          <CardHeader>
            <CardTitle className="text-red-600">Опасная зона</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600 mb-4">
                  Выход из аккаунта. Вам потребуется снова войти.
                </p>
                <Button variant="outline" className="text-red-600 hover:bg-red-50" onClick={handleLogout}>
                  Выйти из аккаунта
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

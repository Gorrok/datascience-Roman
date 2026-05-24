import React, { useState, useEffect } from 'react';
import { api } from './api';
import './App.css';

const tg = window.Telegram.WebApp;

function App() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('plans'); // plans, wishes, create
  const [newPlan, setNewPlan] = useState({
    title: '',
    description: '',
    plan_type: 'wish',
    planned_date: ''
  });

  const userId = tg.initDataUnsafe?.user?.id || 123456; // Для тестирования
  const userName = tg.initDataUnsafe?.user?.first_name || 'User';
  const partnerId = userId === 123456 ? 789012 : 123456; // Второй пользователь
  const partnerName = userId === 123456 ? 'Катя' : 'Роман';

  useEffect(() => {
    tg.ready();
    tg.expand(); // Разворачиваем на весь экран
    tg.enableClosingConfirmation(); // Подтверждение при закрытии
    
    // Настраиваем цвета для Telegram
    tg.setHeaderColor('#ff6b9d');
    tg.setBackgroundColor('#ffeef8');
    
    // Скрываем кнопку назад
    tg.BackButton.hide();
    
    loadPlans();
  }, []);

  const loadPlans = async () => {
    try {
      setLoading(true);
      const data = await api.getPlans(userId, false);
      setPlans(data);
    } catch (error) {
      console.error('Error loading plans:', error);
      tg.showAlert('Ошибка загрузки планов');
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePlan = async () => {
    if (!newPlan.title.trim()) {
      tg.showAlert('Введите название плана');
      return;
    }

    try {
      const planData = {
        ...newPlan,
        created_by_id: userId,
        created_by_name: userName,
        planned_date: newPlan.planned_date || null
      };

      await api.createPlan(planData);
      tg.showPopup({
        message: 'План создан! 🎉',
        buttons: [{ type: 'ok' }]
      });

      setNewPlan({
        title: '',
        description: '',
        plan_type: 'wish',
        planned_date: ''
      });
      setActiveTab('plans');
      loadPlans();
    } catch (error) {
      console.error('Error creating plan:', error);
      tg.showAlert('Ошибка создания плана');
    }
  };

  const handleInvitePartner = async (planId, planTitle) => {
    try {
      await api.createInvite({
        plan_id: planId,
        from_user_id: userId,
        from_user_name: userName,
        to_user_id: partnerId,
        to_user_name: partnerName
      });

      tg.showPopup({
        message: `Приглашение отправлено ${partnerName}! 💌`,
        buttons: [{ type: 'ok' }]
      });
    } catch (error) {
      console.error('Error sending invite:', error);
      tg.showAlert('Ошибка отправки приглашения');
    }
  };

  const handleCompletePlan = async (planId) => {
    try {
      await api.updatePlan(planId, { is_completed: true });
      tg.showPopup({
        message: 'Поздравляем! План выполнен 🎉',
        buttons: [{ type: 'ok' }]
      });
      loadPlans();
    } catch (error) {
      console.error('Error completing plan:', error);
      tg.showAlert('Ошибка обновления плана');
    }
  };

  const handleDeletePlan = async (planId) => {
    tg.showConfirm('Удалить этот план?', async (confirmed) => {
      if (confirmed) {
        try {
          await api.deletePlan(planId);
          loadPlans();
        } catch (error) {
          console.error('Error deleting plan:', error);
          tg.showAlert('Ошибка удаления плана');
        }
      }
    });
  };

  const wishes = plans.filter(p => p.plan_type === 'wish');
  const scheduledPlans = plans.filter(p => p.plan_type === 'plan' && p.planned_date);

  if (loading) {
    return (
      <div className="app">
        <div className="loading">
          <div>Загружаем ваши планы...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <header className="header">
        <h1>💕 Наш планировщик</h1>
        <p>Привет, {userName}!</p>
      </header>

      <nav className="tabs">
        <button
          className={activeTab === 'plans' ? 'active' : ''}
          onClick={() => setActiveTab('plans')}
        >
          📅 Планы ({scheduledPlans.length})
        </button>
        <button
          className={activeTab === 'wishes' ? 'active' : ''}
          onClick={() => setActiveTab('wishes')}
        >
          ✨ Хотелки ({wishes.length})
        </button>
        <button
          className={activeTab === 'create' ? 'active' : ''}
          onClick={() => setActiveTab('create')}
        >
          ➕ Создать
        </button>
      </nav>

      <main className="content">
        {activeTab === 'plans' && (
          <div className="plans-list">
            {scheduledPlans.length === 0 ? (
              <div className="empty" data-emoji="📅">
                <p>Пока нет запланированных событий</p>
                <p>Создайте план и назначьте дату!</p>
              </div>
            ) : (
              scheduledPlans.map(plan => (
                <div key={plan.id} className="plan-card">
                  <div className="plan-header">
                    <h3>{plan.title}</h3>
                    <span className="plan-author">от {plan.created_by_name}</span>
                  </div>
                  {plan.description && (
                    <p className="plan-description">{plan.description}</p>
                  )}
                  {plan.planned_date && (
                    <p className="plan-date">
                      📅 {new Date(plan.planned_date).toLocaleDateString('ru-RU')}
                    </p>
                  )}
                  <div className="plan-actions">
                    <button onClick={() => handleCompletePlan(plan.id)}>
                      ✅ Выполнено
                    </button>
                    {plan.created_by_id === userId && (
                      <>
                        <button onClick={() => handleInvitePartner(plan.id, plan.title)}>
                          💌 Пригласить
                        </button>
                        <button onClick={() => handleDeletePlan(plan.id)} className="delete">
                          🗑️
                        </button>
                      </>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'wishes' && (
          <div className="plans-list">
            {wishes.length === 0 ? (
              <div className="empty" data-emoji="✨">
                <p>Пока нет хотелок</p>
                <p>Добавьте что хотите сделать вместе!</p>
              </div>
            ) : (
              wishes.map(plan => (
                <div key={plan.id} className="plan-card wish">
                  <div className="plan-header">
                    <h3>✨ {plan.title}</h3>
                    <span className="plan-author">от {plan.created_by_name}</span>
                  </div>
                  {plan.description && (
                    <p className="plan-description">{plan.description}</p>
                  )}
                  <div className="plan-actions">
                    <button onClick={() => handleInvitePartner(plan.id, plan.title)}>
                      💌 Пригласить
                    </button>
                    {plan.created_by_id === userId && (
                      <button onClick={() => handleDeletePlan(plan.id)} className="delete">
                        🗑️
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'create' && (
          <div className="create-form">
            <h2>Создать новый план</h2>
            
            <div className="form-group">
              <label>Тип:</label>
              <div className="radio-group">
                <label>
                  <input
                    type="radio"
                    value="wish"
                    checked={newPlan.plan_type === 'wish'}
                    onChange={(e) => setNewPlan({...newPlan, plan_type: e.target.value})}
                  />
                  ✨ Хотелка
                </label>
                <label>
                  <input
                    type="radio"
                    value="plan"
                    checked={newPlan.plan_type === 'plan'}
                    onChange={(e) => setNewPlan({...newPlan, plan_type: e.target.value})}
                  />
                  📅 План
                </label>
              </div>
            </div>

            <div className="form-group">
              <label>Название:</label>
              <input
                type="text"
                placeholder="Например: Сходить в кино"
                value={newPlan.title}
                onChange={(e) => setNewPlan({...newPlan, title: e.target.value})}
              />
            </div>

            <div className="form-group">
              <label>Описание:</label>
              <textarea
                placeholder="Дополнительная информация..."
                value={newPlan.description}
                onChange={(e) => setNewPlan({...newPlan, description: e.target.value})}
                rows="3"
              />
            </div>

            {newPlan.plan_type === 'plan' && (
              <div className="form-group">
                <label>Дата:</label>
                <input
                  type="datetime-local"
                  value={newPlan.planned_date}
                  onChange={(e) => setNewPlan({...newPlan, planned_date: e.target.value})}
                />
              </div>
            )}

            <button className="create-button" onClick={handleCreatePlan}>
              Создать {newPlan.plan_type === 'wish' ? '✨' : '📅'}
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;

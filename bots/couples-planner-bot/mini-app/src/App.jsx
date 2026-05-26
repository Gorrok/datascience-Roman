import React, { useState, useEffect } from 'react';
import { api } from './api';
import './App.css';

const tg = window.Telegram?.WebApp || {
  ready: () => {},
  expand: () => {},
  enableClosingConfirmation: () => {},
  setHeaderColor: () => {},
  setBackgroundColor: () => {},
  BackButton: { hide: () => {} },
  initDataUnsafe: {},
  showAlert: (msg) => alert(msg),
  showConfirm: (msg, cb) => cb(confirm(msg)),
  showPopup: ({ message }) => alert(message),
};

export default function App() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('plans');
  const [newPlan, setNewPlan] = useState({
    title: '',
    description: '',
    plan_type: 'wish',
    planned_date: ''
  });

  const userId = tg.initDataUnsafe?.user?.id || 123456;
  const userName = tg.initDataUnsafe?.user?.first_name || 'User';
  const USER_1_ID = 569520047;
  const USER_2_ID = 290761828;
  const partnerId = userId === USER_1_ID ? USER_2_ID : USER_1_ID;
  const partnerName = userId === USER_1_ID ? 'Катя' : 'Роман';

  useEffect(() => {
    tg.ready();
    tg.expand();
    tg.enableClosingConfirmation();
    tg.setHeaderColor('#1d4ed8');
    tg.setBackgroundColor('#f8fafc');
    tg.BackButton.hide();
    loadPlans();

    const safetyTimeout = setTimeout(() => setLoading(false), 5000);
    return () => clearTimeout(safetyTimeout);
  }, []);

  const loadPlans = async () => {
    try {
      setLoading(true);
      const data = await api.getPlans(userId, false);
      setPlans(data);
    } catch (err) {
      console.error('Failed to load plans:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePlan = async () => {
    if (!newPlan.title.trim()) {
      tg.showAlert('Введите название');
      return;
    }
    try {
      await api.createPlan({
        ...newPlan,
        created_by_id: userId,
        created_by_name: userName,
        planned_date: newPlan.planned_date || null
      });
      setNewPlan({ title: '', description: '', plan_type: 'wish', planned_date: '' });
      setActiveTab('plans');
      loadPlans();
    } catch {
      tg.showAlert('Ошибка при создании');
    }
  };

  const handleInvite = async (planId) => {
    try {
      await api.createInvite({
        plan_id: planId,
        from_user_id: userId,
        from_user_name: userName,
        to_user_id: partnerId,
        to_user_name: partnerName
      });
      tg.showPopup({ message: `Приглашение отправлено — ${partnerName}`, buttons: [{ type: 'ok' }] });
    } catch {
      tg.showAlert('Ошибка при отправке');
    }
  };

  const handleComplete = async (planId) => {
    try {
      await api.updatePlan(planId, { is_completed: true });
      loadPlans();
    } catch {
      tg.showAlert('Ошибка при обновлении');
    }
  };

  const handleDelete = async (planId) => {
    tg.showConfirm('Удалить план?', async (ok) => {
      if (ok) {
        try {
          await api.deletePlan(planId);
          loadPlans();
        } catch {
          tg.showAlert('Ошибка при удалении');
        }
      }
    });
  };

  const wishes = plans.filter(p => p.plan_type === 'wish');
  const scheduledPlans = plans.filter(p => p.plan_type === 'plan');

  if (loading) {
    return (
      <div className="splash">
        <div className="splash-inner">
          <div className="splash-logo">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <rect width="48" height="48" rx="14" fill="#1d4ed8"/>
              <path d="M12 24L20 32L36 16" stroke="white" strokeWidth="3.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </div>
          <div className="splash-title">Планировщик</div>
          <div className="splash-loader"><div></div></div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-bg">
          <div className="header-circle c1"></div>
          <div className="header-circle c2"></div>
          <div className="header-circle c3"></div>
        </div>
        <div className="header-content">
          <div className="header-top">
            <div className="header-logo">
              <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
                <rect width="32" height="32" rx="9" fill="rgba(255,255,255,0.2)"/>
                <path d="M8 16L13 21L24 10" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div className="header-badge">{plans.length} планов</div>
          </div>
          <h1>Привет, {userName}</h1>
          <p>Ваши совместные планы и желания</p>
        </div>
      </header>

      {/* Tabs */}
      <nav className="tabs">
        {[
          { id: 'plans', label: 'Планы', count: scheduledPlans.length },
          { id: 'wishes', label: 'Желания', count: wishes.length },
          { id: 'create', label: 'Создать', count: null },
        ].map(tab => (
          <button
            key={tab.id}
            className={activeTab === tab.id ? 'active' : ''}
            onClick={() => setActiveTab(tab.id)}
          >
            {tab.label}
            {tab.count !== null && <span className="tab-count">{tab.count}</span>}
          </button>
        ))}
      </nav>

      {/* Content */}
      <main className="content">

        {/* Plans */}
        {activeTab === 'plans' && (
          <div>
            {scheduledPlans.length === 0 ? (
              <EmptyState
                title="Нет планов"
                subtitle="Создайте первый совместный план"
                icon="calendar"
              />
            ) : (
              <div className="cards">
                {scheduledPlans.map(plan => (
                  <PlanCard
                    key={plan.id}
                    plan={plan}
                    userId={userId}
                    onInvite={handleInvite}
                    onComplete={handleComplete}
                    onDelete={handleDelete}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* Wishes */}
        {activeTab === 'wishes' && (
          <div>
            {wishes.length === 0 ? (
              <EmptyState
                title="Нет желаний"
                subtitle="Запишите что хотите сделать вместе"
                icon="star"
              />
            ) : (
              <div className="cards">
                {wishes.map(plan => (
                  <PlanCard
                    key={plan.id}
                    plan={plan}
                    userId={userId}
                    onInvite={handleInvite}
                    onComplete={handleComplete}
                    onDelete={handleDelete}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* Create */}
        {activeTab === 'create' && (
          <div className="create-form">
            <div className="form-header">
              <h2>Новый план</h2>
              <p>Заполните детали</p>
            </div>

            <div className="type-selector">
              {[
                { value: 'wish', label: 'Желание', desc: 'Хочу когда-нибудь' },
                { value: 'plan', label: 'План', desc: 'Конкретная дата' },
              ].map(t => (
                <div
                  key={t.value}
                  className={`type-card ${newPlan.plan_type === t.value ? 'active' : ''}`}
                  onClick={() => setNewPlan({ ...newPlan, plan_type: t.value })}
                >
                  <div className="type-dot"></div>
                  <div>
                    <div className="type-label">{t.label}</div>
                    <div className="type-desc">{t.desc}</div>
                  </div>
                </div>
              ))}
            </div>

            <div className="field">
              <label>Название</label>
              <input
                type="text"
                placeholder="Например: поехать в горы"
                value={newPlan.title}
                onChange={e => setNewPlan({ ...newPlan, title: e.target.value })}
              />
            </div>

            <div className="field">
              <label>Описание <span className="optional">необязательно</span></label>
              <textarea
                placeholder="Детали, пожелания, заметки..."
                value={newPlan.description}
                onChange={e => setNewPlan({ ...newPlan, description: e.target.value })}
                rows={3}
              />
            </div>

            {newPlan.plan_type === 'plan' && (
              <div className="field">
                <label>Дата и время</label>
                <input
                  type="datetime-local"
                  value={newPlan.planned_date}
                  onChange={e => setNewPlan({ ...newPlan, planned_date: e.target.value })}
                />
              </div>
            )}

            <button className="submit-btn" onClick={handleCreatePlan}>
              Создать
            </button>
          </div>
        )}
      </main>
    </div>
  );
}

function PlanCard({ plan, userId, onInvite, onComplete, onDelete }) {
  const dateStr = plan.planned_date
    ? new Date(plan.planned_date).toLocaleDateString('ru-RU', {
        day: 'numeric', month: 'long', year: 'numeric'
      })
    : null;

  return (
    <div className="card">
      <div className="card-top">
        <div className="card-meta">
          <span className="card-author">{plan.created_by_name}</span>
          {dateStr && <span className="card-date">{dateStr}</span>}
        </div>
        {plan.created_by_id === userId && (
          <button className="card-delete" onClick={() => onDelete(plan.id)}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        )}
      </div>
      <h3 className="card-title">{plan.title}</h3>
      {plan.description && <p className="card-desc">{plan.description}</p>}
      <div className="card-actions">
        <button className="btn-primary" onClick={() => onComplete(plan.id)}>
          Выполнено
        </button>
        {plan.created_by_id === userId && (
          <button className="btn-secondary" onClick={() => onInvite(plan.id)}>
            Пригласить
          </button>
        )}
      </div>
    </div>
  );
}

function EmptyState({ title, subtitle, icon }) {
  return (
    <div className="empty">
      <div className="empty-icon">
        {icon === 'calendar' ? (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>
          </svg>
        ) : (
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
        )}
      </div>
      <h3>{title}</h3>
      <p>{subtitle}</p>
      <div className="empty-hint">Перейдите во вкладку «Создать»</div>
    </div>
  );
}

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
  HapticFeedback: {
    impactOccurred: () => {},
    notificationOccurred: () => {},
    selectionChanged: () => {},
  },
  initDataUnsafe: {},
  showAlert: (msg) => alert(msg),
  showConfirm: (msg, cb) => cb(confirm(msg)),
  showPopup: ({ message }) => alert(message),
};

const haptic = {
  light:   () => tg.HapticFeedback?.impactOccurred?.('light'),
  medium:  () => tg.HapticFeedback?.impactOccurred?.('medium'),
  heavy:   () => tg.HapticFeedback?.impactOccurred?.('heavy'),
  success: () => tg.HapticFeedback?.notificationOccurred?.('success'),
  error:   () => tg.HapticFeedback?.notificationOccurred?.('error'),
  warn:    () => tg.HapticFeedback?.notificationOccurred?.('warning'),
  select:  () => tg.HapticFeedback?.selectionChanged?.(),
};

const USER_1_ID = 569520047;
const USER_2_ID = 290761828;

function formatDate(dateStr) {
  if (!dateStr) return null;
  const date = new Date(dateStr);
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const target = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  const diffDays = Math.round((target - today) / 86400000);

  let label;
  let tone = 'normal';
  if (diffDays < 0) {
    label = `${Math.abs(diffDays)} дн. назад`;
  } else if (diffDays === 0) {
    label = 'Сегодня';
    tone = 'today';
  } else if (diffDays === 1) {
    label = 'Завтра';
    tone = 'soon';
  } else if (diffDays < 7) {
    label = `Через ${diffDays} дн.`;
    tone = 'soon';
  } else {
    label = date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' });
  }

  return { label, tone, diffDays };
}

function getInitial(name) {
  if (!name) return '?';
  return name.trim().charAt(0).toUpperCase();
}

export default function App() {
  const [plans, setPlans] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('plans');
  const [sheetOpen, setSheetOpen] = useState(false);
  const [newPlan, setNewPlan] = useState({
    title: '',
    description: '',
    plan_type: 'plan',
    planned_date: ''
  });

  const userId = tg.initDataUnsafe?.user?.id || USER_1_ID;
  const userName = tg.initDataUnsafe?.user?.first_name || 'User';
  const partnerName = userId === USER_1_ID ? 'Катя' : 'Роман';
  const partnerId = userId === USER_1_ID ? USER_2_ID : USER_1_ID;

  useEffect(() => {
    tg.ready();
    tg.expand();
    tg.enableClosingConfirmation();
    tg.setHeaderColor('#7c3aed');
    tg.setBackgroundColor('#fefcfa');
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

  const openSheet = (type = 'plan') => {
    haptic.light();
    setNewPlan({ title: '', description: '', plan_type: type, planned_date: '' });
    setSheetOpen(true);
  };

  const closeSheet = () => {
    setSheetOpen(false);
  };

  const handleCreatePlan = async () => {
    if (!newPlan.title.trim()) {
      haptic.error();
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
      haptic.success();
      setNewPlan({ title: '', description: '', plan_type: 'plan', planned_date: '' });
      setSheetOpen(false);
      setActiveTab(newPlan.plan_type === 'wish' ? 'wishes' : 'plans');
      loadPlans();
    } catch {
      haptic.error();
      tg.showAlert('Ошибка при создании');
    }
  };

  const handleInvite = async (planId) => {
    haptic.medium();
    try {
      await api.createInvite({
        plan_id: planId,
        from_user_id: userId,
        from_user_name: userName,
        to_user_id: partnerId,
        to_user_name: partnerName
      });
      haptic.success();
      tg.showPopup({
        message: `Приглашение отправлено — ${partnerName}`,
        buttons: [{ type: 'ok' }],
      });
    } catch {
      haptic.error();
      tg.showAlert('Ошибка при отправке');
    }
  };

  const handleComplete = async (planId) => {
    haptic.success();
    try {
      await api.updatePlan(planId, { is_completed: true });
      loadPlans();
    } catch {
      haptic.error();
      tg.showAlert('Ошибка при обновлении');
    }
  };

  const handleDelete = async (planId) => {
    haptic.warn();
    tg.showConfirm('Удалить план?', async (ok) => {
      if (ok) {
        try {
          await api.deletePlan(planId);
          haptic.success();
          loadPlans();
        } catch {
          haptic.error();
          tg.showAlert('Ошибка при удалении');
        }
      }
    });
  };

  const wishes = plans.filter(p => p.plan_type === 'wish');
  const scheduledPlans = plans.filter(p => p.plan_type === 'plan');

  // Sort plans by date — closest first
  const sortedPlans = [...scheduledPlans].sort((a, b) => {
    if (!a.planned_date) return 1;
    if (!b.planned_date) return -1;
    return new Date(a.planned_date) - new Date(b.planned_date);
  });

  if (loading) {
    return (
      <div className="splash">
        <div className="splash-inner">
          <div className="splash-logo">
            <svg width="56" height="56" viewBox="0 0 56 56" fill="none">
              <rect width="56" height="56" rx="16" fill="rgba(255,255,255,0.2)" />
              <path d="M28 42c-1 0-2-.4-2.7-1.1-3.6-3.5-7-6.6-9.6-9.6-2.6-3-3.7-5.7-3.7-8.3 0-3 1-5.4 2.8-7.2C16.6 14 19 13 22 13c2 0 3.8.6 5.2 1.6.4.3.6.4.8.4.2 0 .4-.1.8-.4C30.2 13.6 32 13 34 13c3 0 5.4 1 7.2 2.8C43 17.6 44 20 44 23c0 2.6-1.1 5.3-3.7 8.3-2.6 3-6 6.1-9.6 9.6-.7.7-1.7 1.1-2.7 1.1z" fill="white"/>
            </svg>
          </div>
          <div className="splash-title">Наши планы</div>
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
              <svg width="36" height="36" viewBox="0 0 36 36" fill="none">
                <rect width="36" height="36" rx="11" fill="rgba(255,255,255,0.2)" />
                <path d="M18 27c-.5 0-1-.2-1.4-.5-2.3-2.2-4.5-4.3-6.2-6.2-1.7-1.9-2.4-3.7-2.4-5.3 0-1.9.6-3.5 1.8-4.6C10.9 9.6 12.4 9 14.3 9c1.3 0 2.4.4 3.3 1 .3.2.4.3.5.3.1 0 .2-.1.5-.3.9-.6 2-1 3.3-1 1.9 0 3.4.6 4.6 1.4 1.1 1.1 1.7 2.7 1.7 4.6 0 1.7-.7 3.4-2.4 5.3-1.7 1.9-3.9 4-6.2 6.2-.4.3-.9.5-1.4.5z" fill="white"/>
              </svg>
            </div>
            <div className="header-badge">{plans.length} {plans.length === 1 ? 'идея' : plans.length < 5 ? 'идеи' : 'идей'}</div>
          </div>
          <h1>Привет, {userName}<span className="heart">♥</span></h1>
          <p>Ваши совместные планы с {partnerName}</p>
        </div>
      </header>

      {/* Tabs */}
      <nav className="tabs">
        {[
          { id: 'plans',  label: 'Планы',   count: scheduledPlans.length },
          { id: 'wishes', label: 'Желания', count: wishes.length },
        ].map(tab => (
          <button
            key={tab.id}
            className={activeTab === tab.id ? 'active' : ''}
            onClick={() => { haptic.select(); setActiveTab(tab.id); }}
          >
            {tab.label}
            <span className="tab-count">{tab.count}</span>
          </button>
        ))}
      </nav>

      {/* Content */}
      <main className="content">

        {activeTab === 'plans' && (
          <>
            {sortedPlans.length === 0 ? (
              <EmptyState
                title="Пока ничего не запланировано"
                subtitle={`Создайте первый план с ${partnerName} — поездку, ужин или свидание`}
                icon="calendar"
              />
            ) : (
              <>
                <div className="section-title">Запланировано</div>
                <div className="cards">
                  {sortedPlans.map(plan => (
                    <PlanCard
                      key={plan.id}
                      plan={plan}
                      userId={userId}
                      userName={userName}
                      partnerName={partnerName}
                      onInvite={handleInvite}
                      onComplete={handleComplete}
                      onDelete={handleDelete}
                    />
                  ))}
                </div>
              </>
            )}
          </>
        )}

        {activeTab === 'wishes' && (
          <>
            {wishes.length === 0 ? (
              <EmptyState
                title="Список желаний пуст"
                subtitle="Запишите, что хотелось бы сделать вместе когда-нибудь"
                icon="star"
              />
            ) : (
              <>
                <div className="section-title">Список желаний</div>
                <div className="cards">
                  {wishes.map(plan => (
                    <PlanCard
                      key={plan.id}
                      plan={plan}
                      userId={userId}
                      userName={userName}
                      partnerName={partnerName}
                      onInvite={handleInvite}
                      onComplete={handleComplete}
                      onDelete={handleDelete}
                    />
                  ))}
                </div>
              </>
            )}
          </>
        )}
      </main>

      {/* FAB */}
      <button className="fab" onClick={() => openSheet(activeTab === 'wishes' ? 'wish' : 'plan')}>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
          <path d="M12 5v14M5 12h14"/>
        </svg>
        Добавить {activeTab === 'wishes' ? 'желание' : 'план'}
      </button>

      {/* Bottom Sheet */}
      {sheetOpen && (
        <div className="sheet-overlay" onClick={(e) => e.target === e.currentTarget && closeSheet()}>
          <div className="sheet">
            <div className="sheet-handle"></div>
            <div className="sheet-header">
              <div className="sheet-header-text">
                <h2>Новая идея</h2>
                <p>Что вы хотите вместе?</p>
              </div>
              <button className="sheet-close" onClick={closeSheet}>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                  <path d="M18 6L6 18M6 6l12 12"/>
                </svg>
              </button>
            </div>

            <div className="create-form">
              <div className="type-selector">
                {[
                  { value: 'plan', label: 'План',    desc: 'С датой' },
                  { value: 'wish', label: 'Желание', desc: 'Когда-нибудь' },
                ].map(t => (
                  <div
                    key={t.value}
                    className={`type-card ${newPlan.plan_type === t.value ? 'active' : ''}`}
                    onClick={() => { haptic.select(); setNewPlan({ ...newPlan, plan_type: t.value }); }}
                  >
                    <div className="type-emoji">
                      {t.value === 'plan' ? (
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <rect x="3" y="4" width="18" height="18" rx="2"/>
                          <path d="M16 2v4M8 2v4M3 10h18"/>
                        </svg>
                      ) : (
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                          <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                        </svg>
                      )}
                    </div>
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
                  autoFocus
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
                  <label>Когда</label>
                  <input
                    type="datetime-local"
                    value={newPlan.planned_date}
                    onChange={e => setNewPlan({ ...newPlan, planned_date: e.target.value })}
                  />
                </div>
              )}

              <button className="submit-btn" onClick={handleCreatePlan}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                  <path d="M20 6L9 17l-5-5"/>
                </svg>
                Создать
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function PlanCard({ plan, userId, userName, partnerName, onInvite, onComplete, onDelete }) {
  const isMine = plan.created_by_id === userId;
  const dateInfo = formatDate(plan.planned_date);
  const cardClass = `card ${dateInfo?.tone === 'soon' || dateInfo?.tone === 'today' ? 'soon' : ''}`;

  return (
    <div className={cardClass}>
      <div className="card-top">
        <div className="card-meta">
          <div className={`author-avatar ${isMine ? '' : 'partner'}`}>
            {getInitial(plan.created_by_name)}
          </div>
          <div className="card-author-info">
            <div className="card-author-name">
              {isMine ? 'Вы' : plan.created_by_name}
            </div>
            {dateInfo && (
              <div className={`card-date ${dateInfo.tone}`}>
                {dateInfo.label}
              </div>
            )}
          </div>
        </div>
        {isMine && (
          <button className="card-delete" onClick={() => onDelete(plan.id)}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        )}
      </div>

      <h3 className="card-title">{plan.title}</h3>
      {plan.description && <p className="card-desc">{plan.description}</p>}

      <div className="card-actions">
        <button className="btn-primary" onClick={() => onComplete(plan.id)}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
          Выполнено
        </button>
        {isMine && (
          <button className="btn-secondary" onClick={() => onInvite(plan.id)}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
              <path d="M22 4L12 14.01l-3-3"/>
            </svg>
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
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2"/>
            <path d="M16 2v4M8 2v4M3 10h18"/>
          </svg>
        ) : (
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
        )}
      </div>
      <h3>{title}</h3>
      <p>{subtitle}</p>
      <div className="empty-hint">Нажмите «Добавить» внизу</div>
    </div>
  );
}

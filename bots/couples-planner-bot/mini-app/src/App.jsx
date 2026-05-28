import React, { useState, useEffect, useRef, useCallback } from 'react';
import { api } from './api';
import './App.css';

const tg = window.Telegram?.WebApp || {
  ready: () => {},
  expand: () => {},
  enableClosingConfirmation: () => {},
  setHeaderColor: () => {},
  setBackgroundColor: () => {},
  BackButton: { hide: () => {}, show: () => {}, onClick: () => {}, offClick: () => {} },
  HapticFeedback: {
    impactOccurred: () => {},
    notificationOccurred: () => {},
    selectionChanged: () => {},
  },
  initDataUnsafe: {},
  showAlert: (msg) => alert(msg),
  showConfirm: (msg, cb) => cb(confirm(msg)),
  showPopup: ({ message }) => alert(message),
  onEvent: () => {},
  offEvent: () => {},
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

const SWEET_MESSAGES = [
  'Ты делаешь меня счастливее',
  'Каждый план с тобой — лучший',
  'Скучаю, даже когда ты рядом',
  'Ты — мой любимый человек',
  'Спасибо, что ты есть',
  'С тобой даже вторник — праздник',
  'Обнимаю крепко-крепко',
  'Хочу все планы только с тобой',
  'Ты — моё самое уютное «домой»',
  'Люблю наши маленькие приключения',
];

const HEART_COLORS = ['#ec4899', '#f59e0b', '#7c3aed', '#f472b6', '#fb7185'];

function formatDate(dateStr) {
  if (!dateStr) return null;
  const date = new Date(dateStr);
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const target = new Date(date.getFullYear(), date.getMonth(), date.getDate());
  const diffDays = Math.round((target - today) / 86400000);

  // Время показываем, только если оно задано (не полночь)
  const hasTime = date.getHours() !== 0 || date.getMinutes() !== 0;
  const timeStr = hasTime
    ? date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
    : null;

  let label;
  let tone = 'normal';
  let overdue = false;

  if (diffDays < 0) {
    label = diffDays === -1 ? 'Вчера' : `${Math.abs(diffDays)} дн. назад`;
    tone = 'overdue';
    overdue = true;
  } else if (diffDays === 0) {
    // Сегодня: если время уже прошло — просрочено
    if (hasTime && date < now) {
      label = 'Сегодня';
      tone = 'overdue';
      overdue = true;
    } else {
      label = 'Сегодня';
      tone = 'today';
    }
  } else if (diffDays === 1) {
    label = 'Завтра';
    tone = 'soon';
  } else if (diffDays < 7) {
    label = `Через ${diffDays} дн.`;
    tone = 'soon';
  } else {
    label = date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' });
  }

  if (timeStr) label = `${label} в ${timeStr}`;

  return { label, tone, diffDays, overdue };
}

function formatCompletedDate(dateStr) {
  if (!dateStr) return null;
  const date = new Date(dateStr);
  return date.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
}

function getInitial(name) {
  if (!name) return '?';
  return name.trim().charAt(0).toUpperCase();
}

// Form ↔ datetime-local helpers: <input type="datetime-local"> ожидает 'YYYY-MM-DDTHH:mm'
function toLocalInput(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  const pad = n => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

export default function App() {
  const [plans, setPlans] = useState([]);
  const [completed, setCompleted] = useState([]);
  const [invites, setInvites] = useState([]);
  const [stats, setStats] = useState({ total: 0, completed: 0, plans: 0, wishes: 0, pending_invites: 0 });
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [activeTab, setActiveTab] = useState('plans');
  const [sheetOpen, setSheetOpen] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [hearts, setHearts] = useState([]);
  const [toast, setToast] = useState(null);
  const [form, setForm] = useState({
    title: '',
    description: '',
    plan_type: 'plan',
    planned_date: ''
  });

  const userId = tg.initDataUnsafe?.user?.id || USER_1_ID;
  const userName = tg.initDataUnsafe?.user?.first_name || 'User';
  const partnerName = userId === USER_1_ID ? 'Катя' : 'Роман';
  const partnerId = userId === USER_1_ID ? USER_2_ID : USER_1_ID;

  const loadAll = useCallback(async (silent = false) => {
    if (!silent) setLoading(true);
    try {
      const [activePlans, completedPlans, pendingInvites, statsData] = await Promise.all([
        api.getPlans(userId, { includeCompleted: false }),
        api.getPlans(userId, { onlyCompleted: true }),
        api.getInvites(userId, 'pending'),
        api.getStats(userId),
      ]);
      setPlans(activePlans);
      setCompleted(completedPlans);
      setInvites(pendingInvites);
      setStats(statsData);
    } catch (err) {
      console.error('Failed to load:', err);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [userId]);

  useEffect(() => {
    tg.ready();
    tg.expand();
    tg.enableClosingConfirmation();
    tg.setHeaderColor('#7c3aed');
    tg.setBackgroundColor('#fefcfa');
    tg.BackButton.hide();
    loadAll();
    const safetyTimeout = setTimeout(() => setLoading(false), 5000);
    return () => clearTimeout(safetyTimeout);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── Авто-синхронизация: подтягиваем изменения партнёра ──
  useEffect(() => {
    const syncIfVisible = () => {
      if (document.visibilityState === 'visible') loadAll(true);
    };
    document.addEventListener('visibilitychange', syncIfVisible);
    window.addEventListener('focus', syncIfVisible);
    tg.onEvent?.('activated', syncIfVisible);

    const interval = setInterval(syncIfVisible, 30000);

    return () => {
      document.removeEventListener('visibilitychange', syncIfVisible);
      window.removeEventListener('focus', syncIfVisible);
      tg.offEvent?.('activated', syncIfVisible);
      clearInterval(interval);
    };
  }, [loadAll]);

  // ── Pull-to-refresh ────────────────────────
  const contentRef = useRef(null);
  const pullState = useRef({ startY: 0, pulling: false, distance: 0 });
  const [pullDistance, setPullDistance] = useState(0);

  const onTouchStart = (e) => {
    if (window.scrollY > 0) return;
    pullState.current.startY = e.touches[0].clientY;
    pullState.current.pulling = true;
  };

  const onTouchMove = (e) => {
    if (!pullState.current.pulling) return;
    const dy = e.touches[0].clientY - pullState.current.startY;
    if (dy > 0 && window.scrollY === 0) {
      const dist = Math.min(dy * 0.5, 100);
      pullState.current.distance = dist;
      setPullDistance(dist);
    }
  };

  const onTouchEnd = async () => {
    if (!pullState.current.pulling) return;
    pullState.current.pulling = false;
    if (pullState.current.distance > 60) {
      haptic.medium();
      setRefreshing(true);
      setPullDistance(50);
      await loadAll(true);
    }
    setPullDistance(0);
    pullState.current.distance = 0;
  };

  // ── Сердечки и тосты ───────────────────────
  const burstHearts = (count = 14) => {
    const batch = Array.from({ length: count }).map((_, i) => ({
      id: `${Date.now()}-${i}-${Math.random().toString(36).slice(2, 6)}`,
      left: 8 + Math.random() * 84,
      delay: Math.random() * 0.35,
      duration: 2.2 + Math.random() * 1.4,
      size: 16 + Math.random() * 22,
      drift: (Math.random() - 0.5) * 100,
      color: HEART_COLORS[Math.floor(Math.random() * HEART_COLORS.length)],
    }));
    setHearts(prev => [...prev, ...batch]);
    setTimeout(() => {
      const ids = new Set(batch.map(b => b.id));
      setHearts(prev => prev.filter(h => !ids.has(h.id)));
    }, 4200);
  };

  const showToast = (msg) => {
    setToast(msg);
    setTimeout(() => setToast(t => (t === msg ? null : t)), 2800);
  };

  const onHeartTap = () => {
    haptic.light();
    burstHearts(16);
    showToast(SWEET_MESSAGES[Math.floor(Math.random() * SWEET_MESSAGES.length)]);
  };

  // ── Sheet ──────────────────────────────────
  const openCreateSheet = (type = 'plan') => {
    haptic.light();
    setEditingId(null);
    setForm({ title: '', description: '', plan_type: type, planned_date: '' });
    setSheetOpen(true);
  };

  const openEditSheet = (plan) => {
    haptic.light();
    setEditingId(plan.id);
    setForm({
      title: plan.title || '',
      description: plan.description || '',
      plan_type: plan.plan_type || 'plan',
      planned_date: toLocalInput(plan.planned_date),
    });
    setSheetOpen(true);
  };

  const closeSheet = () => setSheetOpen(false);

  const handleSubmit = async () => {
    if (!form.title.trim()) {
      haptic.error();
      tg.showAlert('Введите название');
      return;
    }
    try {
      if (editingId) {
        await api.updatePlan(editingId, {
          title: form.title,
          description: form.description,
          plan_type: form.plan_type,
          planned_date: form.planned_date || null,
        });
      } else {
        await api.createPlan({
          ...form,
          created_by_id: userId,
          created_by_name: userName,
          planned_date: form.planned_date || null
        });
      }
      haptic.success();
      setSheetOpen(false);
      setEditingId(null);
      setActiveTab(form.plan_type === 'wish' ? 'wishes' : 'plans');
      await loadAll(true);
    } catch {
      haptic.error();
      tg.showAlert('Ошибка при сохранении');
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
        message: `${partnerName} получит приглашение на этот план`,
        buttons: [{ type: 'ok' }],
      });
    } catch {
      haptic.error();
      tg.showAlert('Ошибка при отправке');
    }
  };

  const handleComplete = async (planId) => {
    haptic.success();
    burstHearts(12);
    try {
      await api.updatePlan(planId, { is_completed: true });
      await loadAll(true);
    } catch {
      haptic.error();
      tg.showAlert('Ошибка при обновлении');
    }
  };

  const handleUncomplete = async (planId) => {
    haptic.medium();
    try {
      await api.updatePlan(planId, { is_completed: false });
      await loadAll(true);
    } catch {
      haptic.error();
      tg.showAlert('Ошибка при возврате');
    }
  };

  const handleDelete = async (planId) => {
    haptic.warn();
    tg.showConfirm('Удалить план?', async (ok) => {
      if (ok) {
        try {
          await api.deletePlan(planId);
          haptic.success();
          await loadAll(true);
        } catch {
          haptic.error();
          tg.showAlert('Ошибка при удалении');
        }
      }
    });
  };

  const handleRespondInvite = async (inviteId, status) => {
    haptic.medium();
    try {
      await api.respondToInvite(inviteId, status);
      haptic.success();
      await loadAll(true);
    } catch {
      haptic.error();
      tg.showAlert('Ошибка');
    }
  };

  const wishes = plans.filter(p => p.plan_type === 'wish');
  const scheduledPlans = [...plans.filter(p => p.plan_type === 'plan')].sort((a, b) => {
    if (!a.planned_date) return 1;
    if (!b.planned_date) return -1;
    return new Date(a.planned_date) - new Date(b.planned_date);
  });

  // Группировка планов по близости даты
  const planGroups = (() => {
    const groups = { overdue: [], today: [], week: [], later: [], noDate: [] };
    for (const p of scheduledPlans) {
      const info = formatDate(p.planned_date);
      if (!info) groups.noDate.push(p);
      else if (info.overdue) groups.overdue.push(p);
      else if (info.diffDays === 0) groups.today.push(p);
      else if (info.diffDays < 7) groups.week.push(p);
      else groups.later.push(p);
    }
    return groups;
  })();

  const planSections = [
    { key: 'overdue', title: 'Просрочено',  items: planGroups.overdue },
    { key: 'today',   title: 'Сегодня',     items: planGroups.today },
    { key: 'week',    title: 'На неделе',   items: planGroups.week },
    { key: 'later',   title: 'Позже',       items: planGroups.later },
    { key: 'noDate',  title: 'Без даты',    items: planGroups.noDate },
  ].filter(s => s.items.length > 0);

  const showFab = activeTab === 'plans' || activeTab === 'wishes';

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
    <div
      className="app"
      onTouchStart={onTouchStart}
      onTouchMove={onTouchMove}
      onTouchEnd={onTouchEnd}
    >
      {/* Floating hearts */}
      <div className="hearts-layer">
        {hearts.map(h => (
          <span
            key={h.id}
            className="floating-heart"
            style={{
              left: `${h.left}%`,
              fontSize: `${h.size}px`,
              color: h.color,
              animationDuration: `${h.duration}s`,
              animationDelay: `${h.delay}s`,
              '--drift': `${h.drift}px`,
            }}
          >♥</span>
        ))}
      </div>

      {/* Sweet toast */}
      {toast && (
        <div className="sweet-toast" key={toast}>
          <span className="sweet-toast-heart">♥</span>
          {toast}
        </div>
      )}

      {/* Pull-to-refresh indicator */}
      {(pullDistance > 0 || refreshing) && (
        <div
          className="pull-indicator"
          style={{
            transform: `translateX(-50%) translateY(${Math.min(pullDistance, 60)}px)`,
            opacity: Math.min(pullDistance / 60, 1),
          }}
        >
          <div className={`pull-spinner ${refreshing ? 'spinning' : ''}`}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
              <path d="M21 12a9 9 0 1 1-3-6.7L21 8"/>
              <path d="M21 3v5h-5"/>
            </svg>
          </div>
        </div>
      )}

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
            <div className="header-badge">с {partnerName}</div>
          </div>

          <h1>
            Привет, {userName}
            <span className="heart" onClick={onHeartTap} role="button" aria-label="Сердечко">♥</span>
          </h1>

          <div className="stats-row">
            <div className="stat">
              <div className="stat-num">{stats.completed}</div>
              <div className="stat-label">вместе сделали</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat">
              <div className="stat-num">{stats.plans}</div>
              <div className="stat-label">в планах</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat">
              <div className="stat-num">{stats.wishes}</div>
              <div className="stat-label">желаний</div>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <nav className="tabs four">
        {[
          { id: 'plans',     label: 'Планы',    count: scheduledPlans.length },
          { id: 'wishes',    label: 'Желания',  count: wishes.length },
          { id: 'invites',   label: 'Зовут',    count: invites.length, pulse: invites.length > 0 },
          { id: 'completed', label: 'История',  count: completed.length },
        ].map(tab => (
          <button
            key={tab.id}
            className={activeTab === tab.id ? 'active' : ''}
            onClick={() => { haptic.select(); setActiveTab(tab.id); }}
          >
            {tab.label}
            <span className={`tab-count ${tab.pulse ? 'pulse' : ''}`}>{tab.count}</span>
          </button>
        ))}
      </nav>

      {/* Content */}
      <main className="content" ref={contentRef}>

        {activeTab === 'plans' && (
          <>
            {scheduledPlans.length === 0 ? (
              <EmptyState
                title="Пока ничего не запланировано"
                subtitle={`Создайте первый план с ${partnerName} — поездку, ужин или свидание`}
                icon="calendar"
              />
            ) : (
              planSections.map(section => (
                <div key={section.key}>
                  <div className={`section-title ${section.key === 'overdue' ? 'overdue' : ''}`}>
                    {section.title}
                  </div>
                  <div className="cards">
                    {section.items.map(plan => (
                      <PlanCard
                        key={plan.id}
                        plan={plan}
                        userId={userId}
                        onInvite={handleInvite}
                        onComplete={handleComplete}
                        onEdit={openEditSheet}
                        onDelete={handleDelete}
                      />
                    ))}
                  </div>
                </div>
              ))
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
                      onInvite={handleInvite}
                      onComplete={handleComplete}
                      onEdit={openEditSheet}
                      onDelete={handleDelete}
                    />
                  ))}
                </div>
              </>
            )}
          </>
        )}

        {activeTab === 'invites' && (
          <>
            {invites.length === 0 ? (
              <EmptyState
                title="Вас пока никуда не зовут"
                subtitle={`Когда ${partnerName} позовёт вас на план — он появится здесь`}
                icon="mail"
              />
            ) : (
              <>
                <div className="section-title">{partnerName} зовёт вас</div>
                <div className="cards">
                  {invites.map(inv => (
                    <InviteCard
                      key={inv.id}
                      invite={inv}
                      onAccept={() => handleRespondInvite(inv.id, 'accepted')}
                      onDecline={() => handleRespondInvite(inv.id, 'declined')}
                    />
                  ))}
                </div>
              </>
            )}
          </>
        )}

        {activeTab === 'completed' && (
          <>
            {completed.length === 0 ? (
              <EmptyState
                title="История пока пуста"
                subtitle="Здесь будут все выполненные планы и реализованные желания"
                icon="check"
              />
            ) : (
              <>
                <div className="section-title">{completed.length} {completed.length === 1 ? 'выполнено' : 'выполнено вместе'}</div>
                <div className="cards">
                  {completed.map(plan => (
                    <CompletedCard
                      key={plan.id}
                      plan={plan}
                      userId={userId}
                      onUncomplete={handleUncomplete}
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
      {showFab && (
        <button className="fab" onClick={() => openCreateSheet(activeTab === 'wishes' ? 'wish' : 'plan')}>
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <path d="M12 5v14M5 12h14"/>
          </svg>
          Добавить {activeTab === 'wishes' ? 'желание' : 'план'}
        </button>
      )}

      {/* Bottom Sheet */}
      {sheetOpen && (
        <div className="sheet-overlay" onClick={(e) => e.target === e.currentTarget && closeSheet()}>
          <div className="sheet">
            <div className="sheet-handle"></div>
            <div className="sheet-header">
              <div className="sheet-header-text">
                <h2>{editingId ? 'Редактировать' : 'Новая идея'}</h2>
                <p>{editingId ? 'Измените детали' : 'Что вы хотите вместе?'}</p>
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
                    className={`type-card ${form.plan_type === t.value ? 'active' : ''}`}
                    onClick={() => { haptic.select(); setForm({ ...form, plan_type: t.value }); }}
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
                  value={form.title}
                  onChange={e => setForm({ ...form, title: e.target.value })}
                  autoFocus={!editingId}
                />
              </div>

              <div className="field">
                <label>Описание <span className="optional">необязательно</span></label>
                <textarea
                  placeholder="Детали, пожелания, заметки..."
                  value={form.description}
                  onChange={e => setForm({ ...form, description: e.target.value })}
                  rows={3}
                />
              </div>

              {form.plan_type === 'plan' && (
                <div className="field">
                  <label>Когда</label>
                  <input
                    type="datetime-local"
                    value={form.planned_date}
                    onChange={e => setForm({ ...form, planned_date: e.target.value })}
                  />
                </div>
              )}

              <button className="submit-btn" onClick={handleSubmit}>
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                  <path d="M20 6L9 17l-5-5"/>
                </svg>
                {editingId ? 'Сохранить' : 'Создать'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function PlanCard({ plan, userId, onInvite, onComplete, onEdit, onDelete }) {
  const isMine = plan.created_by_id === userId;
  const dateInfo = formatDate(plan.planned_date);
  const cardClass = `card ${
    dateInfo?.tone === 'overdue' ? 'overdue'
    : (dateInfo?.tone === 'soon' || dateInfo?.tone === 'today') ? 'soon'
    : ''
  }`;

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
          <div className="card-icons">
            <button className="card-icon-btn" onClick={() => onEdit(plan)} aria-label="Редактировать">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
              </svg>
            </button>
            <button className="card-icon-btn danger" onClick={() => onDelete(plan.id)} aria-label="Удалить">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
                <path d="M18 6L6 18M6 6l12 12"/>
              </svg>
            </button>
          </div>
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
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/>
              <path d="M13.73 21a2 2 0 0 1-3.46 0"/>
            </svg>
            Позвать
          </button>
        )}
      </div>
    </div>
  );
}

function InviteCard({ invite, onAccept, onDecline }) {
  const dateInfo = invite.plan?.planned_date ? formatDate(invite.plan.planned_date) : null;

  return (
    <div className="card invite-card">
      <div className="card-top">
        <div className="card-meta">
          <div className="author-avatar partner">
            {getInitial(invite.from_user_name)}
          </div>
          <div className="card-author-info">
            <div className="card-author-name">
              {invite.from_user_name} зовёт вас
            </div>
            <div className="card-date">
              {new Date(invite.created_at).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' })}
            </div>
          </div>
        </div>
      </div>

      {invite.plan?.title && <h3 className="card-title">{invite.plan.title}</h3>}
      {invite.plan?.description && <p className="card-desc">{invite.plan.description}</p>}
      {dateInfo && <div className={`card-date inline ${dateInfo.tone}`}>{dateInfo.label}</div>}

      <div className="card-actions">
        <button className="btn-primary" onClick={onAccept}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
          Я за!
        </button>
        <button className="btn-decline" onClick={onDecline}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
            <path d="M18 6L6 18M6 6l12 12"/>
          </svg>
          Не сейчас
        </button>
      </div>
    </div>
  );
}

function CompletedCard({ plan, userId, onUncomplete, onDelete }) {
  const isMine = plan.created_by_id === userId;
  const completedStr = formatCompletedDate(plan.completed_at);

  return (
    <div className="card completed-card">
      <div className="card-top">
        <div className="card-meta">
          <div className={`author-avatar ${isMine ? '' : 'partner'}`}>
            {getInitial(plan.created_by_name)}
          </div>
          <div className="card-author-info">
            <div className="card-author-name">
              {isMine ? 'Вы' : plan.created_by_name}
            </div>
            {completedStr && <div className="card-date">{completedStr}</div>}
          </div>
        </div>
        <div className="completed-badge">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round">
            <path d="M20 6L9 17l-5-5"/>
          </svg>
        </div>
      </div>

      <h3 className="card-title completed-title">{plan.title}</h3>
      {plan.description && <p className="card-desc">{plan.description}</p>}

      <div className="card-actions">
        <button className="btn-secondary" onClick={() => onUncomplete(plan.id)}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
            <path d="M21 12a9 9 0 1 1-3-6.7L21 8"/>
            <path d="M21 3v5h-5"/>
          </svg>
          Вернуть
        </button>
        {isMine && (
          <button className="card-icon-btn danger inline" onClick={() => onDelete(plan.id)}>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round">
              <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
            </svg>
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
        {icon === 'calendar' && (
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2"/>
            <path d="M16 2v4M8 2v4M3 10h18"/>
          </svg>
        )}
        {icon === 'star' && (
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
          </svg>
        )}
        {icon === 'mail' && (
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
            <path d="M22 6L12 13 2 6"/>
          </svg>
        )}
        {icon === 'check' && (
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
            <path d="M22 4L12 14.01l-3-3"/>
          </svg>
        )}
      </div>
      <h3>{title}</h3>
      <p>{subtitle}</p>
    </div>
  );
}

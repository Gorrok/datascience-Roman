#!/usr/bin/python3
"""
Универсальная логика получения данных для отчетов групп
Используется для групп: ЛУЧ, MAXIMUM, MORE
"""

import pymysql
from datetime import datetime, timedelta

# СПИСКИ МЕНЕДЖЕРОВ ПО ГРУППАМ
LUCH_MANAGERS = [
    'Егор Петров', 'Александр Голубов', 'Юлия Трифонова',
    'Седа Барсегян', 'Эдуард Осин'
]

MAXIMUM_MANAGERS = [
    'Надежда Данилова', 'Ольга Фролова', 'Анна Савёлова',
    'Максим Прокофьев', 'Егор Храновский'
]

MORE_MANAGERS = [
    'Иван Солоненко', 'Ульяна Процюк', 'Владислав Какорин',
    'Маргарита Осипова', 'Михаил Мордвин'
]

# АКТИВНЫЕ СТАТУСЫ ВОРОНКИ
ACTIVE_STATUSES = (
    13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522,
    13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966,
    49345819, 13560999, 14338762, 13561008, 142, 143
)


def execute_query(connection, query, error_message, params=None):
    """Выполнение SQL запроса с параметрами для безопасности"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"❌ Ошибка выполнения запроса {error_message}: {e}")
        return []


def get_week_dates():
    """Получить даты текущей недели (понедельник - воскресенье)"""
    today = datetime.now()
    days_since_monday = today.weekday()  # 0=понедельник, 6=воскресенье
    monday = today - timedelta(days=days_since_monday)
    sunday = monday + timedelta(days=6)
    return monday, sunday


def get_month_dates():
    """Получить даты текущего месяца для сделок"""
    today = datetime.now()
    month_start = today.replace(day=1)
    if month_start.month == 12:
        next_month = month_start.replace(year=month_start.year + 1, month=1, day=1)
    else:
        next_month = month_start.replace(month=month_start.month + 1, day=1)
    month_end = next_month - timedelta(days=1)
    return month_start, month_end


def get_monthly_deals_for_team(connection, month_start, month_end, managers_tuple):
    """
    Получить сделки за месяц по списку менеджеров
    
    Args:
        connection: соединение с БД
        month_start: начало месяца (datetime)
        month_end: конец месяца (datetime)
        managers_tuple: кортеж имен менеджеров
    
    Returns:
        dict: {имя_менеджера: количество_сделок}
    """
    month_start_str = month_start.strftime('%Y-%m-%d')
    month_end_str = month_end.strftime('%Y-%m-%d')
    
    query = """
    SELECT Ima_otvetstvennogo, COUNT(*) AS count
    FROM Leads
    WHERE DATE(CLSD) BETWEEN %s AND %s
      AND ID_statusa IN %s
      AND Ima_otvetstvennogo IN %s
    GROUP BY Ima_otvetstvennogo
    ORDER BY COUNT(*) DESC
    """
    
    results = execute_query(connection, query, "сделки за месяц",
                          (month_start_str, month_end_str, ACTIVE_STATUSES, managers_tuple))
    
    return {row['Ima_otvetstvennogo']: row['count'] for row in results}


def get_monthly_deals_by_all_teams(connection, month_start, month_end):
    """
    Получить сделки по каждой команде за месяц
    
    Returns:
        dict: {'luch': X, 'maximum': Y, 'more': Z}
    """
    month_start_str = month_start.strftime('%Y-%m-%d')
    month_end_str = month_end.strftime('%Y-%m-%d')
    
    deals_by_team = {}
    
    query = """
    SELECT COUNT(*) AS count
    FROM Leads
    WHERE DATE(CLSD) BETWEEN %s AND %s
      AND ID_statusa IN %s
      AND Ima_otvetstvennogo IN %s
    """
    
    # Сделки ЛУЧ
    luch_deals = execute_query(connection, query, "сделки группы ЛУЧ",
                              (month_start_str, month_end_str, ACTIVE_STATUSES, tuple(LUCH_MANAGERS)))
    deals_by_team['luch'] = luch_deals[0]['count'] if luch_deals else 0
    
    # Сделки MAXIMUM
    maximum_deals = execute_query(connection, query, "сделки группы MAXIMUM",
                                  (month_start_str, month_end_str, ACTIVE_STATUSES, tuple(MAXIMUM_MANAGERS)))
    deals_by_team['maximum'] = maximum_deals[0]['count'] if maximum_deals else 0
    
    # Сделки MORE
    more_deals = execute_query(connection, query, "сделки группы MORE",
                              (month_start_str, month_end_str, ACTIVE_STATUSES, tuple(MORE_MANAGERS)))
    deals_by_team['more'] = more_deals[0]['count'] if more_deals else 0
    
    return deals_by_team


def get_weekly_first_meetings_for_team(connection, week_start, week_end, managers_tuple):
    """
    Получить проведенные первые встречи за неделю по списку менеджеров
    
    Returns:
        dict: {имя_менеджера: количество_встреч}
    """
    week_start_str = week_start.strftime('%Y-%m-%d')
    week_end_str = week_end.strftime('%Y-%m-%d')
    
    query = """
    SELECT Ima_otvetstvennogo, COUNT(*) AS count
    FROM Leads
    WHERE DATE(Data_provedennoj_pervoj_vstreci) BETWEEN %s AND %s
      AND Ima_otvetstvennogo IN %s
    GROUP BY Ima_otvetstvennogo
    ORDER BY COUNT(*) DESC
    """
    
    results = execute_query(connection, query, "первые встречи за неделю",
                          (week_start_str, week_end_str, managers_tuple))
    
    return {row['Ima_otvetstvennogo']: row['count'] for row in results}


def get_weekly_repeat_meetings_for_team(connection, week_start, week_end, managers_tuple):
    """
    Получить повторные встречи за неделю по списку менеджеров
    
    Returns:
        dict: {имя_менеджера: количество_встреч}
    """
    week_start_str = week_start.strftime('%Y-%m-%d')
    week_end_str = week_end.strftime('%Y-%m-%d')
    
    query = """
    SELECT Ima_otvetstvennogo, COUNT(*) AS count
    FROM Leads
    WHERE DATE(Data_provedennoj_vtoroj_vstreci) BETWEEN %s AND %s
      AND Ima_otvetstvennogo IN %s
    GROUP BY Ima_otvetstvennogo
    ORDER BY COUNT(*) DESC
    """
    
    results = execute_query(connection, query, "повторные встречи за неделю",
                          (week_start_str, week_end_str, managers_tuple))
    
    return {row['Ima_otvetstvennogo']: row['count'] for row in results}


def get_weekly_bookings_for_team(connection, week_start, week_end, managers_tuple):
    """
    Получить брони за неделю по списку менеджеров
    
    Returns:
        dict: {имя_менеджера: количество_броней}
    """
    week_start_str = week_start.strftime('%Y-%m-%d')
    week_end_str = week_end.strftime('%Y-%m-%d')
    
    query = """
    SELECT Ima_otvetstvennogo, COUNT(*) AS count
    FROM Leads
    WHERE DATE(Data_postanovki_broni) BETWEEN %s AND %s
      AND Ima_otvetstvennogo IN %s
      AND Ima_otvetstvennogo != 'Никита Подворный'
    GROUP BY Ima_otvetstvennogo
    ORDER BY COUNT(*) DESC
    """
    
    results = execute_query(connection, query, "брони за неделю",
                          (week_start_str, week_end_str, managers_tuple))
    
    return {row['Ima_otvetstvennogo']: row['count'] for row in results}


def get_weekly_bookings_by_all_teams(connection, week_start, week_end):
    """
    Получить брони по каждой команде за неделю
    
    Returns:
        dict: {'luch': X, 'maximum': Y, 'more': Z}
    """
    week_start_str = week_start.strftime('%Y-%m-%d')
    week_end_str = week_end.strftime('%Y-%m-%d')
    
    bookings_by_team = {}
    
    query = """
    SELECT COUNT(*) AS count
    FROM Leads
    WHERE DATE(Data_postanovki_broni) BETWEEN %s AND %s
      AND Ima_otvetstvennogo IN %s
      AND Ima_otvetstvennogo != 'Никита Подворный'
    """
    
    # Брони ЛУЧ
    luch_bookings = execute_query(connection, query, "брони группы ЛУЧ",
                                 (week_start_str, week_end_str, tuple(LUCH_MANAGERS)))
    bookings_by_team['luch'] = luch_bookings[0]['count'] if luch_bookings else 0
    
    # Брони MAXIMUM
    maximum_bookings = execute_query(connection, query, "брони группы MAXIMUM",
                                    (week_start_str, week_end_str, tuple(MAXIMUM_MANAGERS)))
    bookings_by_team['maximum'] = maximum_bookings[0]['count'] if maximum_bookings else 0
    
    # Брони MORE
    more_bookings = execute_query(connection, query, "брони группы MORE",
                                 (week_start_str, week_end_str, tuple(MORE_MANAGERS)))
    bookings_by_team['more'] = more_bookings[0]['count'] if more_bookings else 0
    
    return bookings_by_team


# ПРИМЕР ИСПОЛЬЗОВАНИЯ:
if __name__ == "__main__":
    # Настройки базы данных
    DB_CONFIG = {
        'host': 'rc1d-qrdcittatnft9rs7.mdb.yandexcloud.net',
        'user': 'amocrm_integration',
        'password': 'uoMMuA-@eGjX2_k7se.J',
        'database': 'amocrm_integration',
        'charset': 'utf8mb4',
        'ssl': {'ssl': {}}
    }
    
    # Подключение к БД
    connection = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    
    # Получение дат
    week_start, week_end = get_week_dates()
    month_start, month_end = get_month_dates()
    
    # Пример: получение данных для группы ЛУЧ
    luch_managers_tuple = tuple(LUCH_MANAGERS)
    
    # Сделки ЛУЧ за месяц
    luch_deals = get_monthly_deals_for_team(connection, month_start, month_end, luch_managers_tuple)
    print("Сделки ЛУЧ:", luch_deals)
    
    # Сделки всех команд
    all_deals = get_monthly_deals_by_all_teams(connection, month_start, month_end)
    print("Сделки всех команд:", all_deals)
    
    # Первые встречи ЛУЧ за неделю
    luch_meetings = get_weekly_first_meetings_for_team(connection, week_start, week_end, luch_managers_tuple)
    print("Первые встречи ЛУЧ:", luch_meetings)
    
    # Повторные встречи ЛУЧ за неделю
    luch_repeat = get_weekly_repeat_meetings_for_team(connection, week_start, week_end, luch_managers_tuple)
    print("Повторные встречи ЛУЧ:", luch_repeat)
    
    # Брони ЛУЧ за неделю
    luch_bookings = get_weekly_bookings_for_team(connection, week_start, week_end, luch_managers_tuple)
    print("Брони ЛУЧ:", luch_bookings)
    
    # Брони всех команд
    all_bookings = get_weekly_bookings_by_all_teams(connection, week_start, week_end)
    print("Брони всех команд:", all_bookings)
    
    connection.close()


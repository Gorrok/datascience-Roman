#!/usr/bin/python3
"""
Ежедневные отчеты по группам: ЛУЧ, MAXIMUM, MORE
Интеграция с n8n для автоматизированных отчетов в Telegram
"""

import pymysql
from datetime import datetime, timedelta
from group_reports_data import (
    LUCH_MANAGERS, MAXIMUM_MANAGERS, MORE_MANAGERS, ACTIVE_STATUSES,
    execute_query
)

# АКТИВНЫЕ СТАТУСЫ ВОРОНКИ (из основного файла)
ACTIVE_STATUSES = (
    13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522,
    13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966,
    49345819, 13560999, 14338762, 13561008, 142, 143
)

# TELEGRAM CHAT IDs для групп
TELEGRAM_CHATS = {
    'луч': '-4832660589',       # chat_id конференции группы ЛУЧ
    'maximum': '-5089210322',   # chat_id конференции группы MAXIMUM
    'more': '-5053517827'       # chat_id конференции группы MORE
}


def get_yesterday_date():
    """Получить дату вчерашнего дня"""
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')


def get_daily_metrics_for_team(connection, yesterday_date, managers_tuple, team_name):
    """
    Получить ежедневные метрики для команды

    Returns:
        dict: {
            'team_name': str,
            'yesterday': str,
            'total_first_meetings': int,
            'total_second_meetings': int,
            'total_appointed_meetings': int,
            'total_bookings': int,
            'total_deals': int,
            'total_qualified_leads': int,
            'total_taken_leads': int,
            'clients_in_work': int,
            'first_meetings': list[dict],
            'second_meetings': list[dict],
            'appointed_meetings': list[dict],
            'bookings': list[dict],
            'deals': list[dict],
            'qualified_leads': list[dict],
            'taken_leads': list[dict]
        }
    """

    # SQL запросы для ежедневных метрик
    queries = {
        'total_first_meetings': """
            SELECT COUNT(*) as count FROM Leads
            WHERE DATE(Data_provedennoj_pervoj_vstreci) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
        """,

        'total_second_meetings': """
            SELECT COUNT(*) as count FROM Leads
            WHERE DATE(Data_provedennoj_vtoroj_vstreci) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
        """,

        'total_appointed_meetings': """
            SELECT COUNT(*) as count FROM Leads
            WHERE DATE(Data_naznacenia_pervoj_vstreci) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
        """,

        'total_bookings': """
            SELECT COUNT(*) as count FROM Leads
            WHERE DATE(Data_postanovki_broni) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
        """,

        'total_deals': """
            SELECT COUNT(*) as count FROM Leads
            WHERE DATE(CLSD) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
        """,

        'total_qualified_leads': """
            SELECT COUNT(*) as count FROM Leads
            WHERE DATE(Data_peredaci_v_OP) = %s
            AND Dengi_na_rukah >= 1000000
            AND ID_statusa NOT IN (142, 143)
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
        """,

        'total_taken_leads': """
            SELECT COUNT(*) as count FROM Leads
            WHERE DATE(Data_peredaci_v_OP) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
        """,

        'clients_in_work': """
            SELECT COUNT(*) as count FROM Leads
            WHERE ID_voronki = 437595
            AND CLSD IS NULL
            AND ID_statusa NOT IN (142, 143)
            AND Ima_otvetstvennogo IN %s
        """
    }

    # Детальные запросы по менеджерам (топ-10)
    detail_queries = {
        'first_meetings': """
            SELECT Ima_otvetstvennogo, COUNT(*) as count
            FROM Leads
            WHERE DATE(Data_provedennoj_pervoj_vstreci) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
            GROUP BY Ima_otvetstvennogo
            HAVING count > 0
            ORDER BY count DESC
            LIMIT 10
        """,

        'second_meetings': """
            SELECT Ima_otvetstvennogo, COUNT(*) as count
            FROM Leads
            WHERE DATE(Data_provedennoj_vtoroj_vstreci) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
            GROUP BY Ima_otvetstvennogo
            HAVING count > 0
            ORDER BY count DESC
            LIMIT 10
        """,

        'appointed_meetings': """
            SELECT Ima_otvetstvennogo, COUNT(*) as count
            FROM Leads
            WHERE DATE(Data_naznacenia_pervoj_vstreci) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
            GROUP BY Ima_otvetstvennogo
            HAVING count > 0
            ORDER BY count DESC
            LIMIT 10
        """,

        'bookings': """
            SELECT Ima_otvetstvennogo,
                   COUNT(*) as total_count,
                   SUM(CASE WHEN Bron = 'Платная' THEN 1 ELSE 0 END) as paid_count,
                   SUM(CASE WHEN Bron = 'Бесплатная' THEN 1 ELSE 0 END) as free_count
            FROM Leads
            WHERE DATE(Data_postanovki_broni) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
            GROUP BY Ima_otvetstvennogo
            HAVING total_count > 0
            ORDER BY total_count DESC
            LIMIT 10
        """,

        'deals': """
            SELECT Ima_otvetstvennogo, COUNT(*) as count
            FROM Leads
            WHERE DATE(CLSD) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
            GROUP BY Ima_otvetstvennogo
            HAVING count > 0
            ORDER BY count DESC
            LIMIT 10
        """,

        'qualified_leads': """
            SELECT Ima_otvetstvennogo, COUNT(*) as count
            FROM Leads
            WHERE DATE(Data_peredaci_v_OP) = %s
            AND Dengi_na_rukah >= 1000000
            AND ID_statusa NOT IN (142, 143)
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
            GROUP BY Ima_otvetstvennogo
            HAVING count > 0
            ORDER BY count DESC
            LIMIT 10
        """,

        'taken_leads': """
            SELECT Ima_otvetstvennogo, COUNT(*) as count
            FROM Leads
            WHERE DATE(Data_peredaci_v_OP) = %s
            AND ID_statusa IN %s
            AND Ima_otvetstvennogo IN %s
            GROUP BY Ima_otvetstvennogo
            HAVING count > 0
            ORDER BY count DESC
            LIMIT 10
        """
    }

    # Получаем данные
    result = {
        'team_name': team_name.upper(),
        'yesterday': yesterday_date,
        'chat_id': TELEGRAM_CHATS.get(team_name.lower(), ''),
        'total_first_meetings': 0,
        'total_second_meetings': 0,
        'total_appointed_meetings': 0,
        'total_bookings': 0,
        'total_deals': 0,
        'total_qualified_leads': 0,
        'total_taken_leads': 0,
        'clients_in_work': 0,
        'first_meetings': [],
        'second_meetings': [],
        'appointed_meetings': [],
        'bookings': [],
        'deals': [],
        'qualified_leads': [],
        'taken_leads': []
    }

    # Получаем totals
    for metric, query in queries.items():
        if metric == 'clients_in_work':
            # Для клиентов в работе нет фильтра по дате
            params = (managers_tuple,)
        else:
            params = (yesterday_date, ACTIVE_STATUSES, managers_tuple)

        data = execute_query(connection, query, f"total {metric}", params)
        result[metric] = data[0]['count'] if data else 0

    # Получаем детальные данные по менеджерам
    for metric, query in detail_queries.items():
        params = (yesterday_date, ACTIVE_STATUSES, managers_tuple)
        data = execute_query(connection, query, f"detail {metric}", params)

        if metric == 'bookings':
            result[metric] = [
                {'name': row['Ima_otvetstvennogo'], 'count': row['total_count'],
                 'paid': row['paid_count'], 'free': row['free_count']}
                for row in data
            ]
        else:
            result[metric] = [
                {'name': row['Ima_otvetstvennogo'], 'count': row['count']}
                for row in data
            ]

    return result


def get_all_groups_daily_reports(connection):
    """
    Получить ежедневные отчеты для всех групп

    Returns:
        dict: {
            'luch': dict_with_data,
            'maximum': dict_with_data,
            'more': dict_with_data
        }
    """
    yesterday_date = get_yesterday_date()

    reports = {}

    # Отчет для группы ЛУЧ
    luch_data = get_daily_metrics_for_team(
        connection, yesterday_date, tuple(LUCH_MANAGERS), 'ЛУЧ'
    )
    reports['luch'] = luch_data

    # Отчет для группы MAXIMUM
    maximum_data = get_daily_metrics_for_team(
        connection, yesterday_date, tuple(MAXIMUM_MANAGERS), 'MAXIMUM'
    )
    reports['maximum'] = maximum_data

    # Отчет для группы MORE
    more_data = get_daily_metrics_for_team(
        connection, yesterday_date, tuple(MORE_MANAGERS), 'MORE'
    )
    reports['more'] = more_data

    return reports


# Функции для n8n интеграции
def get_luch_daily_report(connection):
    """Получить ежедневный отчет для группы ЛУЧ"""
    yesterday_date = get_yesterday_date()
    return get_daily_metrics_for_team(
        connection, yesterday_date, tuple(LUCH_MANAGERS), 'ЛУЧ'
    )


def get_maximum_daily_report(connection):
    """Получить ежедневный отчет для группы MAXIMUM"""
    yesterday_date = get_yesterday_date()
    return get_daily_metrics_for_team(
        connection, yesterday_date, tuple(MAXIMUM_MANAGERS), 'MAXIMUM'
    )


def get_more_daily_report(connection):
    """Получить ежедневный отчет для группы MORE"""
    yesterday_date = get_yesterday_date()
    return get_daily_metrics_for_team(
        connection, yesterday_date, tuple(MORE_MANAGERS), 'MORE'
    )


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

    # Получение всех отчетов
    all_reports = get_all_groups_daily_reports(connection)

    for group_name, report in all_reports.items():
        print(f"\n=== ОТЧЕТ ГРУППЫ {group_name.upper()} ===")
        print(f"Дата: {report['yesterday']}")
        print(f"Первые встречи: {report['total_first_meetings']}")
        print(f"Повторные встречи: {report['total_second_meetings']}")
        print(f"Назначенные встречи: {report['total_appointed_meetings']}")
        print(f"Брони: {report['total_bookings']}")
        print(f"Сделки: {report['total_deals']}")
        print(f"Квалифицированные заявки: {report['total_qualified_leads']}")
        print(f"Взятые в работу: {report['total_taken_leads']}")
        print(f"Клиентов в работе: {report['clients_in_work']}")
        print(f"Chat ID: {report['chat_id']}")

    connection.close()
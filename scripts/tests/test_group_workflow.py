#!/usr/bin/python3
"""
Тестовый скрипт для проверки работы кода групп в workflow
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

# TELEGRAM CHAT IDs
TELEGRAM_CHATS = {
    'луч': '-4832660589',
    'maximum': '-5089210322',
    'more': '-5053517827'
}

def execute_query(connection, query, error_message, params=None):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
    except pymysql.MySQLError as e:
        print(f"❌ Ошибка выполнения запроса {error_message}: {e}")
        return []

def get_yesterday_date():
    yesterday = datetime.now() - timedelta(days=1)
    return yesterday.strftime('%Y-%m-%d')

def get_daily_metrics_for_team(connection, yesterday_date, managers_tuple, team_name):
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
        'clients_in_work': 0
    }

    # Получаем totals
    for metric, query in queries.items():
        if metric == 'clients_in_work':
            params = (managers_tuple,)
        else:
            params = (yesterday_date, ACTIVE_STATUSES, managers_tuple)

        data = execute_query(connection, query, f"total {metric}", params)
        result[metric] = data[0]['count'] if data else 0

    return result

# Тестирование
if __name__ == "__main__":
    DB_CONFIG = {
        'host': 'rc1d-qrdcittatnft9rs7.mdb.yandexcloud.net',
        'user': 'amocrm_integration',
        'password': 'uoMMuA-@eGjX2_k7se.J',
        'database': 'amocrm_integration',
        'charset': 'utf8mb4',
        'ssl': {'ssl': {}}
    }

    connection = pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)
    yesterday_date = get_yesterday_date()

    # Тестируем все группы
    groups = [
        ('ЛУЧ', LUCH_MANAGERS),
        ('MAXIMUM', MAXIMUM_MANAGERS),
        ('MORE', MORE_MANAGERS)
    ]

    for team_name, managers in groups:
        print(f"\n=== ТЕСТИРОВАНИЕ ГРУППЫ {team_name} ===")
        try:
            result = get_daily_metrics_for_team(
                connection, yesterday_date, tuple(managers), team_name
            )
            print(f"✅ Группа {team_name}: {result['total_first_meetings']} первых встреч")
            print(f"   Chat ID: {result['chat_id']}")
        except Exception as e:
            print(f"❌ Ошибка в группе {team_name}: {e}")

    connection.close()
    print("\n🎉 Тестирование завершено!")
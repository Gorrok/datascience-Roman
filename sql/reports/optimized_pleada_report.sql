-- Оптимизированный единый запрос для отчета PLEADA
-- Собирает все метрики одним запросом за вчерашний день

WITH yesterday_data AS (
    SELECT
        Ima_otvetstvennogo,
        ID_statusa,
        Bron,
        Data_provedennoj_pervoj_vstreci,
        Data_provedennoj_vtoroj_vstreci,
        Data_naznacenia_pervoj_vstreci,
        Data_postanovki_broni,
        CLSD,
        Data_peredaci_v_OP,
        Dengi_na_rukah,
        ID_voronki
    FROM Leads
    WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
    AND Ima_otvetstvennogo IS NOT NULL
    AND Ima_otvetstvennogo != ""
    AND Ima_otvetstvennogo != "Никита Пестерев"
    -- Условие для вчерашней даты (для оптимизации индексов)
    AND (
        DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    )
),

-- Агрегированные данные по ответственным
aggregated_data AS (
    SELECT
        Ima_otvetstvennogo,

        -- Первые встречи
        COUNT(CASE WHEN DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as first_meetings_count,

        -- Повторные встречи
        COUNT(CASE WHEN DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as second_meetings_count,

        -- Назначенные встречи
        COUNT(CASE WHEN DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as appointed_meetings_count,

        -- Брони (платные/бесплатные)
        COUNT(CASE WHEN DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Bron = "Платная" THEN 1 END) as paid_bookings,
        COUNT(CASE WHEN DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Bron = "Бесплатная" THEN 1 END) as free_bookings,
        COUNT(CASE WHEN DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as total_bookings,

        -- Сделки
        COUNT(CASE WHEN DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as deals_count,

        -- Квалифицированные лиды (от 1 млн)
        COUNT(CASE WHEN DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
                   AND Dengi_na_rukah >= 1000000
                   AND ID_statusa NOT IN (142, 143) THEN 1 END) as qualified_leads_count,

        -- Взятые в работу лиды
        COUNT(CASE WHEN DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as taken_leads_count

    FROM yesterday_data
    GROUP BY Ima_otvetstvennogo
),

-- Топ-5 менеджеров по каждой метрике
top_managers AS (
    SELECT
        'first_meetings' as metric_type,
        Ima_otvetstvennogo,
        first_meetings_count as count_value,
        ROW_NUMBER() OVER (ORDER BY first_meetings_count DESC) as rank_num
    FROM aggregated_data
    WHERE first_meetings_count > 0

    UNION ALL

    SELECT
        'second_meetings' as metric_type,
        Ima_otvetstvennogo,
        second_meetings_count as count_value,
        ROW_NUMBER() OVER (ORDER BY second_meetings_count DESC) as rank_num
    FROM aggregated_data
    WHERE second_meetings_count > 0

    UNION ALL

    SELECT
        'appointed_meetings' as metric_type,
        Ima_otvetstvennogo,
        appointed_meetings_count as count_value,
        ROW_NUMBER() OVER (ORDER BY appointed_meetings_count DESC) as rank_num
    FROM aggregated_data
    WHERE appointed_meetings_count > 0

    UNION ALL

    SELECT
        'bookings' as metric_type,
        Ima_otvetstvennogo,
        total_bookings as count_value,
        ROW_NUMBER() OVER (ORDER BY total_bookings DESC) as rank_num
    FROM aggregated_data
    WHERE total_bookings > 0

    UNION ALL

    SELECT
        'deals' as metric_type,
        Ima_otvetstvennogo,
        deals_count as count_value,
        ROW_NUMBER() OVER (ORDER BY deals_count DESC) as rank_num
    FROM aggregated_data
    WHERE deals_count > 0

    UNION ALL

    SELECT
        'qualified_leads' as metric_type,
        Ima_otvetstvennogo,
        qualified_leads_count as count_value,
        ROW_NUMBER() OVER (ORDER BY qualified_leads_count DESC) as rank_num
    FROM aggregated_data
    WHERE qualified_leads_count > 0

    UNION ALL

    SELECT
        'taken_leads' as metric_type,
        Ima_otvetstvennogo,
        taken_leads_count as count_value,
        ROW_NUMBER() OVER (ORDER BY taken_leads_count DESC) as rank_num
    FROM aggregated_data
    WHERE taken_leads_count > 0
)

-- Финальный результат: топ-5 по каждой метрике + агрегированные итоги
SELECT
    -- Общие итоги
    (SELECT SUM(first_meetings_count) FROM aggregated_data) as total_first_meetings,
    (SELECT SUM(second_meetings_count) FROM aggregated_data) as total_second_meetings,
    (SELECT SUM(appointed_meetings_count) FROM aggregated_data) as total_appointed_meetings,
    (SELECT SUM(total_bookings) FROM aggregated_data) as total_bookings,
    (SELECT SUM(deals_count) FROM aggregated_data) as total_deals,
    (SELECT SUM(qualified_leads_count) FROM aggregated_data) as total_qualified_leads,
    (SELECT SUM(taken_leads_count) FROM aggregated_data) as total_taken_leads,

    -- Клиенты в работе (отдельный подсчет)
    (SELECT COUNT(*) FROM Leads
     WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
     AND Data_peredaci_v_OP IS NOT NULL
     AND CLSD IS NULL
     AND ID_voronki = 437595
     AND Ima_otvetstvennogo IS NOT NULL
     AND Ima_otvetstvennogo != ""
     AND Ima_otvetstvennogo != "Никита Пестерев") as clients_in_work,

    -- Детальные данные по топ-менеджерам
    tm.metric_type,
    tm.Ima_otvetstvennogo,
    tm.count_value,

    -- Для броней добавляем детали по типам
    CASE
        WHEN tm.metric_type = 'bookings' THEN
            (SELECT CONCAT('П:', paid_bookings, ', Б:', free_bookings)
             FROM aggregated_data
             WHERE Ima_otvetstvennogo = tm.Ima_otvetstvennogo)
        ELSE NULL
    END as booking_details

FROM top_managers tm
WHERE rank_num <= 5
ORDER BY
    CASE tm.metric_type
        WHEN 'first_meetings' THEN 1
        WHEN 'second_meetings' THEN 2
        WHEN 'appointed_meetings' THEN 3
        WHEN 'bookings' THEN 4
        WHEN 'deals' THEN 5
        WHEN 'qualified_leads' THEN 6
        WHEN 'taken_leads' THEN 7
    END,
    rank_num;

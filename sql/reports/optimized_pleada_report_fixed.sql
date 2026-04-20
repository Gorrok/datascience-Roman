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
    AND (
        DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        OR DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    )
),

aggregated_data AS (
    SELECT
        Ima_otvetstvennogo,
        COUNT(CASE WHEN DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as first_meetings_count,
        COUNT(CASE WHEN DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as second_meetings_count,
        COUNT(CASE WHEN DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as appointed_meetings_count,
        COUNT(CASE WHEN DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Bron = "Платная" THEN 1 END) as paid_bookings,
        COUNT(CASE WHEN DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Bron = "Бесплатная" THEN 1 END) as free_bookings,
        COUNT(CASE WHEN DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as total_bookings,
        COUNT(CASE WHEN DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as deals_count,
        COUNT(CASE WHEN DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
                   AND Dengi_na_rukah >= 1000000
                   AND ID_statusa NOT IN (142, 143) THEN 1 END) as qualified_leads_count,
        COUNT(CASE WHEN DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as taken_leads_count
    FROM yesterday_data
    GROUP BY Ima_otvetstvennogo
),

top_managers AS (
    SELECT 'first_meetings' as metric_type, Ima_otvetstvennogo, first_meetings_count as count_value,
           ROW_NUMBER() OVER (ORDER BY first_meetings_count DESC) as rank_num
    FROM aggregated_data WHERE first_meetings_count > 0
    UNION ALL
    SELECT 'second_meetings', Ima_otvetstvennogo, second_meetings_count,
           ROW_NUMBER() OVER (ORDER BY second_meetings_count DESC)
    FROM aggregated_data WHERE second_meetings_count > 0
    UNION ALL
    SELECT 'appointed_meetings', Ima_otvetstvennogo, appointed_meetings_count,
           ROW_NUMBER() OVER (ORDER BY appointed_meetings_count DESC)
    FROM aggregated_data WHERE appointed_meetings_count > 0
    UNION ALL
    SELECT 'bookings', Ima_otvetstvennogo, total_bookings,
           ROW_NUMBER() OVER (ORDER BY total_bookings DESC)
    FROM aggregated_data WHERE total_bookings > 0
    UNION ALL
    SELECT 'deals', Ima_otvetstvennogo, deals_count,
           ROW_NUMBER() OVER (ORDER BY deals_count DESC)
    FROM aggregated_data WHERE deals_count > 0
    UNION ALL
    SELECT 'qualified_leads', Ima_otvetstvennogo, qualified_leads_count,
           ROW_NUMBER() OVER (ORDER BY qualified_leads_count DESC)
    FROM aggregated_data WHERE qualified_leads_count > 0
    UNION ALL
    SELECT 'taken_leads', Ima_otvetstvennogo, taken_leads_count,
           ROW_NUMBER() OVER (ORDER BY taken_leads_count DESC)
    FROM aggregated_data WHERE taken_leads_count > 0
),

-- Финальный результат: сначала totals, потом метрики
final_result AS (
    -- Строка с итогами
    SELECT
        (SELECT SUM(first_meetings_count) FROM aggregated_data) as total_first_meetings,
        (SELECT SUM(second_meetings_count) FROM aggregated_data) as total_second_meetings,
        (SELECT SUM(appointed_meetings_count) FROM aggregated_data) as total_appointed_meetings,
        (SELECT SUM(total_bookings) FROM aggregated_data) as total_bookings,
        (SELECT SUM(deals_count) FROM aggregated_data) as total_deals,
        (SELECT SUM(qualified_leads_count) FROM aggregated_data) as total_qualified_leads,
        (SELECT SUM(taken_leads_count) FROM aggregated_data) as total_taken_leads,
        (SELECT COUNT(*) FROM Leads
         WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
         AND Data_peredaci_v_OP IS NOT NULL
         AND CLSD IS NULL
         AND ID_voronki = 437595
         AND Ima_otvetstvennogo IS NOT NULL
         AND Ima_otvetstvennogo != ""
         AND Ima_otvetstvennogo != "Никита Пестерев") as clients_in_work,
        NULL as metric_type,
        NULL as Ima_otvetstvennogo,
        NULL as count_value,
        NULL as booking_details,
        0 as sort_order

    UNION ALL

    -- Строки с метриками
    SELECT
        NULL as total_first_meetings,
        NULL as total_second_meetings,
        NULL as total_appointed_meetings,
        NULL as total_bookings,
        NULL as total_deals,
        NULL as total_qualified_leads,
        NULL as total_taken_leads,
        NULL as clients_in_work,
        tm.metric_type,
        tm.Ima_otvetstvennogo,
        tm.count_value,
        CASE
            WHEN tm.metric_type = 'bookings' THEN
                (SELECT CONCAT('П:', paid_bookings, ', Б:', free_bookings)
                 FROM aggregated_data
                 WHERE Ima_otvetstvennogo = tm.Ima_otvetstvennogo)
            ELSE NULL
        END as booking_details,
        CASE tm.metric_type
            WHEN 'first_meetings' THEN 1
            WHEN 'second_meetings' THEN 2
            WHEN 'appointed_meetings' THEN 3
            WHEN 'bookings' THEN 4
            WHEN 'deals' THEN 5
            WHEN 'qualified_leads' THEN 6
            WHEN 'taken_leads' THEN 7
        END as sort_order
    FROM top_managers tm
    WHERE rank_num <= 5
)

SELECT
    total_first_meetings,
    total_second_meetings,
    total_appointed_meetings,
    total_bookings,
    total_deals,
    total_qualified_leads,
    total_taken_leads,
    clients_in_work,
    metric_type,
    Ima_otvetstvennogo,
    count_value,
    booking_details
FROM final_result
ORDER BY sort_order, count_value DESC;

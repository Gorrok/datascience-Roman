-- SQL запрос, возвращающий JSON с всеми данными
SELECT
    JSON_OBJECT(
        'totals', JSON_OBJECT(
            'first_meetings', (SELECT SUM(first_meetings_count) FROM (
                SELECT COUNT(CASE WHEN DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as first_meetings_count
                FROM Leads
                WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
                AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
                GROUP BY Ima_otvetstvennogo
            ) t),
            'second_meetings', (SELECT SUM(second_meetings_count) FROM (
                SELECT COUNT(CASE WHEN DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as second_meetings_count
                FROM Leads
                WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
                AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
                GROUP BY Ima_otvetstvennogo
            ) t),
            'appointed_meetings', (SELECT SUM(appointed_meetings_count) FROM (
                SELECT COUNT(CASE WHEN DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as appointed_meetings_count
                FROM Leads
                WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
                AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
                GROUP BY Ima_otvetstvennogo
            ) t),
            'bookings', (SELECT SUM(total_bookings) FROM (
                SELECT COUNT(CASE WHEN DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as total_bookings
                FROM Leads
                WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
                AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
                GROUP BY Ima_otvetstvennogo
            ) t),
            'deals', (SELECT SUM(deals_count) FROM (
                SELECT COUNT(CASE WHEN DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as deals_count
                FROM Leads
                WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
                AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
                GROUP BY Ima_otvetstvennogo
            ) t),
            'qualified_leads', (SELECT SUM(qualified_leads_count) FROM (
                SELECT COUNT(CASE WHEN DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
                               AND Dengi_na_rukah >= 1000000
                               AND ID_statusa NOT IN (142, 143) THEN 1 END) as qualified_leads_count
                FROM Leads
                WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
                AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
                GROUP BY Ima_otvetstvennogo
            ) t),
            'taken_leads', (SELECT SUM(taken_leads_count) FROM (
                SELECT COUNT(CASE WHEN DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as taken_leads_count
                FROM Leads
                WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
                AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
                GROUP BY Ima_otvetstvennogo
            ) t),
            'clients_in_work', (SELECT COUNT(*) FROM Leads
             WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
             AND Data_peredaci_v_OP IS NOT NULL
             AND CLSD IS NULL
             AND ID_voronki = 437595
             AND Ima_otvetstvennogo IS NOT NULL
             AND Ima_otvetstvennogo != ''
             AND Ima_otvetstvennogo != 'Никита Пестерев')
        ),
        'metrics', JSON_OBJECT(
            'first_meetings', (SELECT JSON_ARRAYAGG(
                JSON_OBJECT('name', Ima_otvetstvennogo, 'count', first_meetings_count)
            ) FROM (
                SELECT Ima_otvetstvennogo, COUNT(CASE WHEN DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as first_meetings_count
                FROM Leads
                WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
                AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
                GROUP BY Ima_otvetstvennogo
                HAVING first_meetings_count > 0
                ORDER BY first_meetings_count DESC
                LIMIT 5
            ) t),
            'second_meetings', (SELECT JSON_ARRAYAGG(
                JSON_OBJECT('name', Ima_otvetstvennogo, 'count', second_meetings_count)
            ) FROM (
                SELECT Ima_otvetstvennogo, COUNT(CASE WHEN DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN 1 END) as second_meetings_count
                FROM Leads
                WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
                AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
                GROUP BY Ima_otvetstvennogo
                HAVING second_meetings_count > 0
                ORDER BY second_meetings_count DESC
                LIMIT 5
            ) t)
        )
    ) as report_data

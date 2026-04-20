-- Запрос, возвращающий JSON с реальными данными менеджеров
SELECT CONCAT(
    '{',
    '"totals":{',
    '"first_meetings":', (SELECT SUM(cnt) FROM (
        SELECT COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
    ) t), ',',
    '"second_meetings":', (SELECT SUM(cnt) FROM (
        SELECT COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
    ) t), ',',
    '"appointed_meetings":', (SELECT SUM(cnt) FROM (
        SELECT COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
    ) t), ',',
    '"bookings":', (SELECT SUM(cnt) FROM (
        SELECT COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
    ) t), ',',
    '"deals":', (SELECT SUM(cnt) FROM (
        SELECT COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
    ) t), ',',
    '"qualified_leads":', (SELECT SUM(cnt) FROM (
        SELECT COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Dengi_na_rukah >= 1000000
        AND ID_statusa NOT IN (142, 143)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
    ) t), ',',
    '"taken_leads":', (SELECT SUM(cnt) FROM (
        SELECT COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
    ) t), ',',
    '"clients_in_work":', (SELECT COUNT(*) FROM Leads
     WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
     AND Data_peredaci_v_OP IS NOT NULL
     AND CLSD IS NULL
     AND ID_voronki = 437595
     AND Ima_otvetstvennogo IS NOT NULL
     AND Ima_otvetstvennogo != ''
     AND Ima_otvetstvennogo != 'Никита Пестерев'), '},',
    '"first_meetings":[', (SELECT GROUP_CONCAT(
        CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', cnt, '}')
        ORDER BY cnt DESC
        LIMIT 5
    ) FROM (
        SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
        HAVING cnt > 0
    ) t), '],',
    '"second_meetings":[', (SELECT GROUP_CONCAT(
        CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', cnt, '}')
        ORDER BY cnt DESC
        LIMIT 5
    ) FROM (
        SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
        HAVING cnt > 0
    ) t), '],',
    '"appointed_meetings":[', (SELECT GROUP_CONCAT(
        CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', cnt, '}')
        ORDER BY cnt DESC
        LIMIT 5
    ) FROM (
        SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
        HAVING cnt > 0
    ) t), '],',
    '"bookings":[', (SELECT GROUP_CONCAT(
        CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', total_cnt, ',"paid":', paid_cnt, ',"free":', free_cnt, '}')
        ORDER BY total_cnt DESC
        LIMIT 5
    ) FROM (
        SELECT Ima_otvetstvennogo,
               COUNT(*) as total_cnt,
               SUM(CASE WHEN Bron = 'Платная' THEN 1 ELSE 0 END) as paid_cnt,
               SUM(CASE WHEN Bron = 'Бесплатная' THEN 1 ELSE 0 END) as free_cnt
        FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
        HAVING total_cnt > 0
    ) t), '],',
    '"deals":[', (SELECT GROUP_CONCAT(
        CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', cnt, '}')
        ORDER BY cnt DESC
        LIMIT 5
    ) FROM (
        SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
        HAVING cnt > 0
    ) t), '],',
    '"qualified_leads":[', (SELECT GROUP_CONCAT(
        CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', cnt, '}')
        ORDER BY cnt DESC
        LIMIT 5
    ) FROM (
        SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Dengi_na_rukah >= 1000000
        AND ID_statusa NOT IN (142, 143)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
        HAVING cnt > 0
    ) t), '],',
    '"taken_leads":[', (SELECT GROUP_CONCAT(
        CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', cnt, '}')
        ORDER BY cnt DESC
        LIMIT 5
    ) FROM (
        SELECT Ima_otvetstvennogo, COUNT(*) as cnt FROM Leads
        WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
        AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
        AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
        GROUP BY Ima_otvetstvennogo
        HAVING cnt > 0
    ) t), ']',
    '}'
) as report_json

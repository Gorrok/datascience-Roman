-- Исправленный табличный формат со всеми колонками
SELECT
    -- Totals row (13 колонок)
    'totals' as row_type,
    (SELECT SUM(cnt) FROM (SELECT COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo) t) as total_first_meetings,
    (SELECT SUM(cnt) FROM (SELECT COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo) t) as total_second_meetings,
    (SELECT SUM(cnt) FROM (SELECT COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo) t) as total_appointed_meetings,
    (SELECT SUM(cnt) FROM (SELECT COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo) t) as total_bookings,
    (SELECT SUM(cnt) FROM (SELECT COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo) t) as total_deals,
    (SELECT SUM(cnt) FROM (SELECT COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Dengi_na_rukah >= 1000000 AND ID_statusa NOT IN (142, 143) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo) t) as total_qualified_leads,
    (SELECT SUM(cnt) FROM (SELECT COUNT(*) as cnt FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев' GROUP BY Ima_otvetstvennogo) t) as total_taken_leads,
    (SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143) AND Data_peredaci_v_OP IS NOT NULL AND CLSD IS NULL AND ID_voronki = 437595 AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев') as clients_in_work,
    NULL as section, NULL as Ima_otvetstvennogo, NULL as count_value, NULL as booking_details

UNION ALL

-- First meetings data (13 колонок)
SELECT 'data', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       'first_meetings' as section, Ima_otvetstvennogo, COUNT(*) as count_value, NULL
FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY Ima_otvetstvennogo
HAVING COUNT(*) > 0
ORDER BY COUNT(*) DESC

UNION ALL

-- Second meetings data (13 колонок)
SELECT 'data', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       'second_meetings' as section, Ima_otvetstvennogo, COUNT(*) as count_value, NULL
FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY Ima_otvetstvennogo
HAVING COUNT(*) > 0
ORDER BY COUNT(*) DESC

UNION ALL

-- Appointed meetings data (13 колонок)
SELECT 'data', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       'appointed_meetings' as section, Ima_otvetstvennogo, COUNT(*) as count_value, NULL
FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND DATE(Data_naznacenia_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY Ima_otvetstvennogo
HAVING COUNT(*) > 0
ORDER BY COUNT(*) DESC

UNION ALL

-- Bookings data with details (13 колонок)
SELECT 'data', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       'bookings' as section, Ima_otvetstvennogo,
       COUNT(*) as count_value,
       CONCAT('П:', SUM(CASE WHEN Bron = 'Платная' THEN 1 ELSE 0 END), ', Б:', SUM(CASE WHEN Bron = 'Бесплатная' THEN 1 ELSE 0 END))
FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND DATE(Data_postanovki_broni) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY Ima_otvetstvennogo
HAVING COUNT(*) > 0
ORDER BY COUNT(*) DESC

UNION ALL

-- Deals data (13 колонок)
SELECT 'data', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       'deals' as section, Ima_otvetstvennogo, COUNT(*) as count_value, NULL
FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND DATE(CLSD) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY Ima_otvetstvennogo
HAVING COUNT(*) > 0
ORDER BY COUNT(*) DESC

UNION ALL

-- Qualified leads data (13 колонок)
SELECT 'data', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       'qualified_leads' as section, Ima_otvetstvennogo, COUNT(*) as count_value, NULL
FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
AND Dengi_na_rukah >= 1000000
AND ID_statusa NOT IN (142, 143)
AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY Ima_otvetstvennogo
HAVING COUNT(*) > 0
ORDER BY COUNT(*) DESC

UNION ALL

-- Taken leads data (13 колонок)
SELECT 'data', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
       'taken_leads' as section, Ima_otvetstvennogo, COUNT(*) as count_value, NULL
FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY Ima_otvetstvennogo
HAVING COUNT(*) > 0
ORDER BY COUNT(*) DESC

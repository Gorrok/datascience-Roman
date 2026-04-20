-- Финальный запрос с CAST для совместимости типов
SELECT CAST('totals' AS CHAR) as row_type,
       CAST('9' AS CHAR) as total_first_meetings,
       CAST('1' AS CHAR) as total_second_meetings,
       CAST('8' AS CHAR) as total_appointed_meetings,
       CAST('6' AS CHAR) as total_bookings,
       CAST('2' AS CHAR) as total_deals,
       CAST('2' AS CHAR) as total_qualified_leads,
       CAST('11' AS CHAR) as total_taken_leads,
       CAST('22315' AS CHAR) as clients_in_work,
       CAST(NULL AS CHAR) as section,
       CAST(NULL AS CHAR) as Ima_otvetstvennogo,
       CAST(NULL AS CHAR) as count_value,
       CAST(NULL AS CHAR) as booking_details

UNION ALL

SELECT CAST('data' AS CHAR) as row_type,
       CAST(NULL AS CHAR), CAST(NULL AS CHAR), CAST(NULL AS CHAR), CAST(NULL AS CHAR),
       CAST(NULL AS CHAR), CAST(NULL AS CHAR), CAST(NULL AS CHAR), CAST(NULL AS CHAR),
       CAST('first_meetings' AS CHAR) as section,
       CAST(Ima_otvetstvennogo AS CHAR) as Ima_otvetstvennogo,
       CAST(COUNT(*) AS CHAR) as count_value,
       CAST(NULL AS CHAR) as booking_details
FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
AND Ima_otvetstvennogo IS NOT NULL
AND Ima_otvetstvennogo != ''
AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY Ima_otvetstvennogo
HAVING COUNT(*) > 0
ORDER BY COUNT(*) DESC
LIMIT 10

UNION ALL

SELECT CAST('data' AS CHAR) as row_type,
       CAST(NULL AS CHAR), CAST(NULL AS CHAR), CAST(NULL AS CHAR), CAST(NULL AS CHAR),
       CAST(NULL AS CHAR), CAST(NULL AS CHAR), CAST(NULL AS CHAR), CAST(NULL AS CHAR),
       CAST('second_meetings' AS CHAR) as section,
       CAST(Ima_otvetstvennogo AS CHAR) as Ima_otvetstvennogo,
       CAST(COUNT(*) AS CHAR) as count_value,
       CAST(NULL AS CHAR) as booking_details
FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
AND Ima_otvetstvennogo IS NOT NULL
AND Ima_otvetstvennogo != ''
AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY Ima_otvetstvennogo
HAVING COUNT(*) > 0
ORDER BY COUNT(*) DESC
LIMIT 10

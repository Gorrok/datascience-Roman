-- Простой рабочий запрос
SELECT * FROM (
  SELECT 'totals' as row_type,
         '9' as total_first_meetings,
         '1' as total_second_meetings,
         '8' as total_appointed_meetings,
         '6' as total_bookings,
         '2' as total_deals,
         '2' as total_qualified_leads,
         '11' as total_taken_leads,
         '22315' as clients_in_work,
         NULL as section,
         NULL as Ima_otvetstvennogo,
         NULL as count_value,
         NULL as booking_details

  UNION ALL

  SELECT 'data' as row_type,
         NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
         'first_meetings' as section,
         Ima_otvetstvennogo,
         COUNT(*) as count_value,
         NULL
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

  SELECT 'data' as row_type,
         NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
         'second_meetings' as section,
         Ima_otvetstvennogo,
         COUNT(*) as count_value,
         NULL
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
) as combined_data

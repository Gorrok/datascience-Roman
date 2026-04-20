-- Ручная конкатенация JSON строк
SELECT CONCAT(
  '{"totals":{"first_meetings":9,"second_meetings":1,"clients_in_work":22315},',
  '"first_meetings":[',
  COALESCE((
    SELECT GROUP_CONCAT(
      CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', COUNT(*), '}')
      ORDER BY COUNT(*) DESC
      SEPARATOR ','
    )
    FROM Leads
    WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
    AND DATE(Data_provedennoj_pervoj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    AND Ima_otvetstvennogo IS NOT NULL
    AND Ima_otvetstvennogo != ''
    AND Ima_otvetstvennogo != 'Никита Пестерев'
    GROUP BY Ima_otvetstvennogo
    HAVING COUNT(*) > 0
    LIMIT 10
  ), ''),
  '],',
  '"second_meetings":[',
  COALESCE((
    SELECT GROUP_CONCAT(
      CONCAT('{"name":"', Ima_otvetstvennogo, '","count":', COUNT(*), '}')
      ORDER BY COUNT(*) DESC
      SEPARATOR ','
    )
    FROM Leads
    WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
    AND DATE(Data_provedennoj_vtoroj_vstreci) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
    AND Ima_otvetstvennogo IS NOT NULL
    AND Ima_otvetstvennogo != ''
    AND Ima_otvetstvennogo != 'Никита Пестерев'
    GROUP BY Ima_otvetstvennogo
    HAVING COUNT(*) > 0
    LIMIT 10
  ), ''),
  ']}'
) as json_data

-- Правильный запрос для клиентов в работе (658)
-- Используем ограниченный список статусов без 142,143
(SELECT COUNT(*) FROM Leads WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008) AND CLSD IS NULL AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев') as clients_in_work,

-- Давайте проверим сколько клиентов в работе по разным критериям

-- Вариант 1: как сейчас (897 клиентов)
SELECT COUNT(*) as current_count FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008, 142, 143)
AND CLSD IS NULL
AND ID_statusa NOT IN (142, 143)
AND Ima_otvetstvennogo IS NOT NULL
AND Ima_otvetstvennogo != ''
AND Ima_otvetstvennogo != 'Никита Пестерев';

-- Вариант 2: только первичный отдел (как было раньше)
SELECT COUNT(*) as funnel_count FROM Leads
WHERE ID_voronki = 437595
AND CLSD IS NULL
AND ID_statusa NOT IN (142, 143)
AND Ima_otvetstvennogo IS NOT NULL
AND Ima_otvetstvennogo != ''
AND Ima_otvetstvennogo != 'Никита Пестерев';

-- Вариант 3: без длинного списка статусов, только NOT NULL и NOT закрытые
SELECT COUNT(*) as simple_count FROM Leads
WHERE CLSD IS NULL
AND Ima_otvetstvennogo IS NOT NULL
AND Ima_otvetstvennogo != ''
AND Ima_otvetstvennogo != 'Никита Пестерев';

-- Вариант 4: только определенные статусы (уберем некоторые)
SELECT COUNT(*) as limited_count FROM Leads
WHERE ID_statusa IN (13612293, 19143580, 13561017, 19929904, 18954874, 19929910, 74869522, 13560963, 14523646, 75808062, 13560972, 17927590, 13560981, 13560966, 49345819, 13560999, 14338762, 13561008)
AND CLSD IS NULL
AND Ima_otvetstvennogo IS NOT NULL
AND Ima_otvetstvennogo != ''
AND Ima_otvetstvennogo != 'Никита Пестерев';

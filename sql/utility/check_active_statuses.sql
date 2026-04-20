-- Посчитаем только активные статусы (исключая 142 и 143)
SELECT COUNT(*) as active_clients
FROM Leads
WHERE ID_voronki = 437595
  AND CLSD IS NULL
  AND ID_statusa NOT IN (142, 143)
  AND Ima_otvetstvennogo IS NOT NULL
  AND Ima_otvetstvennogo != ''
  AND Ima_otvetstvennogo != 'Никита Пестерев';

-- А теперь посчитаем клиентов, переданных в ОП
SELECT COUNT(*) as transferred_clients
FROM Leads
WHERE ID_voronki = 437595
  AND Data_peredaci_v_OP IS NOT NULL
  AND CLSD IS NULL
  AND ID_statusa NOT IN (142, 143)
  AND Ima_otvetstvennogo IS NOT NULL
  AND Ima_otvetstvennogo != ''
  AND Ima_otvetstvennogo != 'Никита Пестерев';

-- И переданных в ОП вчера
SELECT COUNT(*) as transferred_yesterday
FROM Leads
WHERE ID_voronki = 437595
  AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY)
  AND CLSD IS NULL
  AND ID_statusa NOT IN (142, 143)
  AND Ima_otvetstvennogo IS NOT NULL
  AND Ima_otvetstvennogo != ''
  AND Ima_otvetstvennogo != 'Никита Пестерев';

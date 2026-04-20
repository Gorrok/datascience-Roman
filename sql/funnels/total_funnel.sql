-- Сколько всего лидов в первичном отделе
SELECT COUNT(*) as total_in_funnel
FROM Leads
WHERE ID_voronki = 437595;

-- Сколько закрытых лидов в первичном отделе
SELECT COUNT(*) as closed_in_funnel
FROM Leads
WHERE ID_voronki = 437595
  AND CLSD IS NOT NULL;

-- Сколько с ответственными в первичном отделе
SELECT COUNT(*) as with_managers_in_funnel
FROM Leads
WHERE ID_voronki = 437595
  AND Ima_otvetstvennogo IS NOT NULL
  AND Ima_otvetstvennogo != ''
  AND Ima_otvetstvennogo != 'Никита Пестерев';

-- Проверим что в первичном отделе
SELECT ID_statusa, COUNT(*) as cnt
FROM Leads
WHERE ID_voronki = 437595
  AND CLSD IS NULL
  AND Ima_otvetstvennogo IS NOT NULL
  AND Ima_otvetstvennogo != ''
  AND Ima_otvetstvennogo != 'Никита Пестерев'
GROUP BY ID_statusa
ORDER BY cnt DESC;

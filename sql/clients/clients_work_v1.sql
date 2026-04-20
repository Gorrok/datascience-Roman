-- Попробуем с фильтром по передаче в ОП
SELECT COUNT(*) as clients_with_transfer
FROM Leads
WHERE ID_voronki = 437595
  AND CLSD IS NULL
  AND ID_statusa NOT IN (142, 143)
  AND Data_peredaci_v_OP IS NOT NULL
  AND Ima_otvetstvennogo IS NOT NULL
  AND Ima_otvetstvennogo != ''
  AND Ima_otvetstvennogo != 'Никита Пестерев';

-- Или только с определенными активными статусами
SELECT COUNT(*) as clients_specific_statuses
FROM Leads
WHERE ID_voronki = 437595
  AND CLSD IS NULL
  AND ID_statusa IN (19143580, 13561017, 19929904, 19929910, 13612293, 74869522, 14523646, 13560963)
  AND Ima_otvetstvennogo IS NOT NULL
  AND Ima_otvetstvennogo != ''
  AND Ima_otvetstvennogo != 'Никита Пестерев';

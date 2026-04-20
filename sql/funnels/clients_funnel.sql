-- Финальный правильный запрос для клиентов в работе (658)
-- Активные этапы первичного отдела кроме статусов 142 и 143
(SELECT COUNT(*) FROM Leads WHERE ID_voronki = 437595 AND CLSD IS NULL AND ID_statusa NOT IN (142, 143) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев') as clients_in_work,

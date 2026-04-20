-- Финальная версия клиентов в работе - переданные в ОП вчера
(SELECT COUNT(*) FROM Leads WHERE ID_voronki = 437595 AND DATE(Data_peredaci_v_OP) = DATE_SUB(CURDATE(), INTERVAL 1 DAY) AND CLSD IS NULL AND ID_statusa NOT IN (142, 143) AND Ima_otvetstvennogo IS NOT NULL AND Ima_otvetstvennogo != '' AND Ima_otvetstvennogo != 'Никита Пестерев') as clients_in_work,

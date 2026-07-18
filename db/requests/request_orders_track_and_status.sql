Выводит все трекеры заказов и их статусы
SELECT track,
       CASE WHEN finished = true THEN 2 
            WHEN cancelled = true THEN -1
            WHEN "inDelivery" = true THEN 1
            ELSE 0
       END AS status
FROM "Orders"
ORDER BY status DESC;

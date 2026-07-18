Задание 1
Ответ: 
SELECT c.login, 
       COUNT(o."inDelivery") AS all_orders_in_delivery, 
       COUNT(o.id) AS distinct_orders_in_delivery
FROM "Couriers" AS c
LEFT JOIN "Orders" AS o ON c.id = o."courierId" AND o."inDelivery" = true
GROUP BY c.login
ORDER BY distinct_orders_in_delivery DESC;

Задание 2
Ответ:
SELECT track,
       CASE WHEN finished = true THEN 2 
            WHEN cancelled = true THEN -1
            WHEN "inDelivery" = true THEN 1
            ELSE 0
       END AS status
FROM "Orders"
ORDER BY status DESC;

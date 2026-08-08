###Выводит список логинов курьеров с количеством их заказов в статусе «В доставке» (поле inDelivery = true).  
SELECT c.login, 
       COUNT(o."inDelivery") AS all_orders_in_delivery, 
       COUNT(o.id) AS distinct_orders_in_delivery
FROM "Couriers" AS c
LEFT JOIN "Orders" AS o ON c.id = o."courierId" AND o."inDelivery" = true
GROUP BY c.login
ORDER BY distinct_orders_in_delivery DESC;

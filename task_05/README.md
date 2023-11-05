List customers who have never placed an order.

Solution 1

    SELECT name as "customers"
    FROM customers
    WHERE customer_id NOT IN (SELECT customer_id FROM orders);

Solution 2

    SELECT name AS "customers"
    FROM customers c
    LEFT JOIN orders o
    ON c.customer_id = o.customer_id
    WHERE o.customer_id IS NULL;

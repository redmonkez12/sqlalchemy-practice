Write a query that will display the customer who has placed the most orders.

    SELECT
        customer_number
    FROM
        orders
    GROUP BY customer_number
    ORDER BY COUNT(*) DESC
    LIMIT 1;
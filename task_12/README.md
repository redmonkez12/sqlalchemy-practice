Write a query that displays the expenditure of each user. Sort the expenditure from highest to lowest.

    SELECT
        s.user_id,
        sum(s.quantity * p.price) AS spending
    FROM sales s
    JOIN product p USING(product_id)
    GROUP BY
        s.user_id
    ORDER BY
        spending DESC,
        s.user_id ASC;  
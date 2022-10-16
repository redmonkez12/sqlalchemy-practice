Napište dotaz, který vypíše utrátu každého uživatele. Seřaďte utrátu od nějvětší po nejmenší.

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
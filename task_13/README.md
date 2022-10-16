Mám tabulku ve které mám customery a jejich idečka objednávek. Chci najít zákazníka,z který si objednal nejvícekrát

    SELECT
        customer_number
    FROM
        orders
    GROUP BY customer_number
    ORDER BY COUNT(*) DESC
    LIMIT 1;
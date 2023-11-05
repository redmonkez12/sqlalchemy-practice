List the customers who were not referred by customer with id 2.

    SELECT name
    FROM customer
    WHERE referee_id <> 2
    OR referee_id IS NULL;

Vypište zákazníky, kteří nebyli doporučení zákazníkem id 2

    SELECT name
    FROM customer
    WHERE referee_id <> 2
    OR referee_id IS NULL;

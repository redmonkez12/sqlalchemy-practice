Vypište největší číslo, které se vyskytuje pouze jednou

    SELECT
        MAX(num) AS num
    FROM
        (SELECT
            num
        FROM
            numbers
        GROUP BY num
        HAVING COUNT(num) = 1) AS t;
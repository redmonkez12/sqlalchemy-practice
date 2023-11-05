List the largest number that appears only once.

    SELECT
        MAX(num) AS num
    FROM
        (SELECT
            num
        FROM
            numbers
        GROUP BY num
        HAVING COUNT(num) = 1) AS t;
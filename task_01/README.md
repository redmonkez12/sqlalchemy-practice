Write a query that finds sellers who have no orders from the company RED.

    SELECT
         s.name
     FROM
         sales_person s
     WHERE
         s.sales_id NOT IN (SELECT
                 o.sales_id
             FROM
                 orders o
                     LEFT JOIN
                 company c USING(company_id)
             WHERE
                 c.name = 'RED');
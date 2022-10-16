Napište dotaz, který najde prodejce, kteří nemají žádnou objednávku u firmy RED

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
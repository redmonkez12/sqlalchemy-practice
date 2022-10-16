Napište dotaz, které vypíše bonus každého zaměstnance. Bonus je 100% mzdy zaměstnance. U zaměstnanců, kteří mají id jako
liché číslo a jméno nezačíná na M vypište bonus a ostatním vypiště bonus 0

    SELECT e.employee_id, COALESCE(ee.salary, 0) AS bonus
    FROM employees e
    LEFT JOIN employees ee ON e.employee_id = ee.employee_id
    AND mod(e.employee_id, 2) = 1
    AND ee.name NOT LIKE 'M%'
    ORDER BY e.employee_id ASC;
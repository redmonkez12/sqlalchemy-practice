Write a query that will display the bonus for each employee. The bonus is 100% of the employee's salary. For employees
with an odd ID and a name that doesn't start with 'M,' display the bonus; for others, display a bonus of 0.

    SELECT e.employee_id, COALESCE(ee.salary, 0) AS bonus
    FROM employees e
    LEFT JOIN employees ee ON e.employee_id = ee.employee_id
    AND mod(e.employee_id, 2) = 1
    AND ee.name NOT LIKE 'M%'
    ORDER BY e.employee_id ASC;
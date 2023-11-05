Find employees with missing information where either the name or salary is missing.

    SELECT employee_id FROM employees WHERE employee_id NOT IN(SELECT employee_id FROM salaries)
    UNION
    SELECT employee_id FROM salaries WHERE employee_id NOT IN(SELECT employee_id FROM employees);

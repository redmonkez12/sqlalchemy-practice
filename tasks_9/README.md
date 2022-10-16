Najděte zaměstnance s chybějícím informacemi u kterých chybí buď jméno a nebo mzda

    SELECT employee_id FROM employees WHERE employee_id NOT IN(SELECT employee_id FROM salaries)
    UNION
    SELECT employee_id FROM salaries WHERE employee_id NOT IN(SELECT employee_id FROM employees);

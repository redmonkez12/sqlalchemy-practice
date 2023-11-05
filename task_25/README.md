List the names of employees and their bonuses where the bonus value is less than 1000.

    CREATE TABLE IF NOT EXISTS employee (
      employee_id bigserial PRIMARY KEY,
      name TEXT NOT NULL,
      supervisor INT,
      salary numeric NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS bonus (
      bonus_id bigserial PRIMARY KEY,
      employee_id bigint NOT NULL,
      bonus numeric,
      CONSTRAINT fk_employee_id
      FOREIGN KEY(employee_id)
      REFERENCES employee(employee_id)
    );
    
    INSERT INTO employee (employee_id, name, supervisor, salary) VALUES
    (3, 'Brad', null, 4000),
    (1, 'John', 3, 1000),
    (2, 'Dan', 3, 2000),
    (4, 'Thomas', 3, 4000);
    
    INSERT INTO bonus (employee_id, bonus) VALUES
    (2, 500),
    (4, 2000);
    
    Řešení 1
    
    SELECT e.name, b.bonus
    FROM employee e
    LEFT JOIN bonus b USING(employee_id)
    WHERE b.bonus < 1000 OR b.bonus IS NULL;
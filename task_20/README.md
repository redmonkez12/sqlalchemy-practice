Write a query that displays the average length of experience for all employees on a specific project. Round to 2 decimal places.

    CREATE TABLE IF NOT EXISTS employee (
      employee_id serial PRIMARY KEY,
      name TEXT NOT NULL,
      experience_years int NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS project (
      project_id serial,
      employee_id serial,
      PRIMARY KEY(project_id, employee_id),
      CONSTRAINT fk_employee_id
      FOREIGN KEY(employee_id)
      REFERENCES employee(employee_id)
    );
    
    INSERT INTO employee (name, experience_years) VALUES
    ('Khaled', 3),
    ('Ali', 2),
    ('John', 1),
    ('Doe', 2);
    
    INSERT INTO project (project_id, employee_id) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 4);
    
    Řešení 1
    
    SELECT
       p.project_id,
       ROUND(AVG(e.experience_years), 2) AS average_years
    FROM project p
    LEFT JOIN employee e USING(employee_id)
    GROUP BY p.project_id;
Najděte velikost týmu každého zaměstnance

    SELECT employee_id, count AS team_size
    FROM Employee
    LEFT JOIN (
        SELECT team_id, COUNT(*) as count
        FROM Employee
        GROUP BY team_id
    ) Team
    ON Team.team_id = Employee.team_id;
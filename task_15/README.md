Write a query that finds the IDs and names of all students who attended a department that no longer exists.

    SELECT student_id, student_name 
    FROM students
    WHERE department_id NOT IN (SELECT department_id from Departments);
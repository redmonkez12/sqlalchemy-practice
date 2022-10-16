Napište dotaz, který najde id a jména všech studentů, kteří chodili na katedru, které už neexistuje

    SELECT student_id, student_name 
    FROM students
    WHERE department_id NOT IN (SELECT department_id from Departments);
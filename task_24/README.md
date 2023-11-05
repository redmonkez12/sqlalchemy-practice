List the subjects that have more than 5 students.
        
    CREATE TABLE courses (
       student_id bigserial PRIMARY KEY,
       student TEXT NOT NULL,
       class TEXT NOT NULL
    );
    
    INSERT INTO courses (student, class) VALUES
    ('A', 'Math'),
    ('B', 'English'),
    ('C', 'Math'),
    ('D', 'Biology'),
    ('E', 'Math'),
    ('F', 'Computer'),
    ('G', 'Math'),
    ('H', 'Math'),
    ('I', 'Math');
    
    Řešení 1
    
    SELECT
        class
    FROM
        courses
    GROUP BY class
    HAVING COUNT(DISTINCT student) >= 5;
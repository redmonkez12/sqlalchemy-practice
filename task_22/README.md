Retrieve actors and directors who have collaborated at least three times.
    
    CREATE TABLE IF NOT EXISTS actor_director(
       actor_id INT NOT NULL,
       director_id INT NOT NULL,
       timestamp INT NOT NULL
    );
    
    INSERT INTO actor_director (actor_id, director_id, timestamp) VALUES
    (1, 1, 0),
    (1, 1, 1),
    (1, 1, 2),
    (1, 2, 3),
    (1, 2, 4),
    (2, 1, 5),
    (2, 1, 6);
    
    Řešení 1
    
    SELECT actor_id, director_id
    FROM actor_director
    GROUP BY actor_id, director_id
    HAVING COUNT(*) >= 3;
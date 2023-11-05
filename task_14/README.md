I want to search for movies that have even IDs and do not have 'boring' in their description.

    SELECT *
    FROM movies
    WHERE mod(id, 2) = 1 AND description <> 'boring'
    ORDER BY rating DESC;
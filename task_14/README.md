Chci vyhledávat jenom filmy, které mají sudé idečko a v popisku nemají boring

    SELECT *
    FROM movies
    WHERE mod(id, 2) = 1 AND description <> 'boring'
    ORDER BY rating DESC;
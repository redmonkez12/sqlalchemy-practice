List the countries that have a land area greater than 3 million square kilometers or at least 25 million inhabitants."

Solution 1

    SELECT w.name, w.population, w.area
    FROM world w
    WHERE w.population >= 25000000 OR w.area >= 3000000;

Solution 2

    SELECT name, population, area
    FROM World
    WHERE population >= 25000000
    
    UNION
    
    SELECT name, population, area
    FROM World
    WHERE area >= 3000000;
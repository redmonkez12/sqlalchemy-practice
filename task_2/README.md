Vypište státy, které mají větší rozlohu než 3 miliony km2 nebo aspoň 25 milionů obyvatel.

Řešení 1

    SELECT w.name, w.population, w.area
    FROM world w
    WHERE w.population >= 25000000 OR w.area >= 3000000;

Řešení 2


    SELECT name, population, area
    FROM World
    WHERE population >= 25000000
    
    UNION
    
    SELECT name, population, area
    FROM World
    WHERE area >= 3000000;
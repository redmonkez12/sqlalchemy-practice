I report the daily number of sold apples and oranges. I want to know the difference in the number of units sold each day.

    CREATE TABLE sales(
      sale_id bigserial PRIMARY KEY,
      sale_date DATE NOT NULL,
      fruit TEXT NOT NULL,
      sold_num int NOT NULL
    );
    
    INSERT INTO sales (sale_date, fruit, sold_num) VALUES
    ('2020-05-01', 'apples', 10),
    ('2020-05-01', 'oranges', 8),
    ('2020-05-02', 'apples', 15),
    ('2020-05-02', 'oranges', 15),
    ('2020-05-03', 'apples', 20),
    ('2020-05-03', 'oranges', 0),
    ('2020-05-04', 'apples', 15),
    ('2020-05-04', 'oranges', 16);
    
    SELECT 
        a.sale_date,
        b.sold_num - a.sold_num as diff
    FROM sales AS a
    JOIN sales AS b on b.sale_date = a.sale_date AND a.fruit != b.fruit
    WHERE b.fruit = 'apples'
    ORDER BY a.sale_date ASC;
Write a query that displays customers who bought an S8 but not an iPhone.

    CREATE TABLE IF NOT EXISTS product (
      product_id serial PRIMARY KEY,
      product_name TEXT NOT NULL,
      unit_price numeric NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS sales (
      seller_id int NOT NULL, 
      product_id int NOT NULL,
      buyer_id int NOT NULL, 
      sale_date DATE NOT NULL,
      quantity int NOT NULL,
      price numeric NOT NULL,
      CONSTRAINT fk_product_id
      FOREIGN KEY(product_id)
      REFeRENCES product(product_id)
    );
    
    
    INSERT INTO product (product_name, unit_price) VALUES
    ('S8', 1000),
    ('G4', 800),
    ('iPhone', 1400);
    
    INSERT INTO sales (seller_id, product_id, buyer_id, sale_date, quantity, price) VALUES
    (1, 1, 1, '2019-01-21', 2, 2000),
    (1, 2, 2, '2019-02-17', 1, 800),
    (2, 1, 3, '2019-06-02', 1, 800),
    (3, 3, 3, '2019-05-13', 2, 2800);
    
    
    Řešení 1
    
    SELECT s.buyer_id
    FROM sales s
    JOIN product p USING(product_id)
    GROUP BY s.buyer_id
    HAVING
    (SUM(CASE WHEN p.product_name = 'S8' THEN 1 ELSE 0 END) > 0 AND
    SUM(CASE WHEN p.product_name = 'iPhone' THEN 1 ELSE 0 END) = 0)
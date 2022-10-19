 Napište dotaz, který vypíše celkové prodané množství pro každý produkt
 
      CREATE TABLE product(
        product_id serial PRIMARY KEY,
        product_name TEXT NOT NULL
      );
      
      CREATE TABLE sales(
        sale_id int NOT NULL,
        product_id int NOT NULL,
        year int NOT NULL,
        quantity int NOT NULL,
        price int NOT NULL,
        PRIMARY KEY(sale_id, year),
        CONSTRAINT fk_product_id
        FOREIGN KEY(product_id)
        REFERENCES product(product_id)
      );
      
      INSERT INTO product (product_id, product_name) VALUES
      (100, 'Nokia'),
      (200, 'Apple'),
      (300, 'Samsung');
      
      INSERT INTO sales (sale_id, product_id, year, quantity, price) VALUES
      (1, 100, 2008, 10, 5000),
      (2, 100, 2009, 12, 5000),
      (7, 200, 2011, 15, 9000);
      
      
      Řešení 1
      
      SELECT product_id, SUM(quantity) AS total_quantity
      FROM Sales
      GROUP BY product_id;


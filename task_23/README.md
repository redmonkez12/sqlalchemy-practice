Write a query that finds users who have logged in for at least five consecutive days. Sort them by ID.

    CREATE TABLE IF NOT EXISTS accounts (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS logins (
      id INT NOT NULL,
      login_date date NOT NULL
    );
    
    INSERT INTO accounts (id, name) VALUES
    (1, 'Winston'),
    (7, 'Jonathan');
    
    INSERT INTO logins (id, login_date) VALUES
    (7, '2020-05-30'),
    (1, '2020-05-30'),
    (7, '2020-05-31'),
    (7, '2020-06-01'),
    (7, '2020-06-02'),
    (7, '2020-06-02'),
    (7, '2020-06-03'),
    (7, '2020-06-07'),
    (1, '2020-06-10');

    WITH t AS (
      SELECT distinct id, login_date
      FROM Logins
    ),
    t1 AS (
    SELECT t.id,
      t.login_date - LAG(t.login_date, 4) OVER (PARTITION by t.id ORDER BY t.login_date) AS count
      FROM t
    )

    SELECT distinct t1.id, a.name
    FROM t1
    JOIN accounts a USING(id)
    WHERE t1.count = 4
    ORDER BY t1.id;
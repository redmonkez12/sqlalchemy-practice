Napiste dotaz ktery vypis stav uctu ktere maji vetsi zustatek nez 10000 kc

    CREATE TABLE users(
     user_id bigserial PRIMARY KEY,
     name TEXT NOT NULL
    );
    
    CREATE TABLE transactions(
     transaction_id bigserial PRIMARY KEY,
      amount numeric NOT NULL,
      transacted_on DATE NOT NULL,
      account_id bigint,
       CONSTRAINT fk_user_id
     FOREIGN KEY(user_id)
     REFERENCES users(user_id)
    );
    
    
    INSERT INTO users (name) VALUES ('Alice'), ('Bob'), ('Charlie');
    
    INSERT INTO transactions (account_id, amount, transacted_on) VALUES
    (1, 7000, '2020-08-01'),
    (1, 7000, '2020-09-01'),
    (1, -3000, '2020-09-02'),
    (2, 1000, '2020-09-12'),
    (3, 6000, '2020-08-07'),
    (3, 6000, '2020-09-07'),
    (3, -4000, '2020-09-11');
    
    SELECT u.name,sum(amount) as balance from transactions t
    JOIN users u
    ON u.account__id = t.account_id
    GROUP BY u.name
    HAVING sum(amount)> 10000;
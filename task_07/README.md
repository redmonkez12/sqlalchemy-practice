Find clients who visited your place but didn't make any transactions. Display the number of visits.

    SELECT v.customer_id, COUNT(v.visit_id) As count_no_trans
    FROM visits v
    LEFT JOIN transactions t USING(visit_id)
    WHERE t.transaction_id IS NULL
    GROUP BY v.customer_id;
Najdětě klienty, kteří byli u vás na návštěvě, ale neprovedli žádnou transakci. Vypište počet návštěv

    SELECT v.customer_id, COUNT(v.visit_id) As count_no_trans
    FROM visits v
    LEFT JOIN transactions t USING(visit_id)
    WHERE t.transaction_id IS NULL
    GROUP BY v.customer_id;
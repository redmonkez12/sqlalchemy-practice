Napište dotaz, který najde uživatele, který byl aktivní 30 dní po sobě do data 2019-07-07 včetně

    SELECT activity_date AS "day",
    COUNT(DISTINCT user_id) AS "active_users"
    FROM activity
    WHERE activity_date > '2019-06-27' AND activity_date <= '2019-07-27'
    GROUP BY activity_date;
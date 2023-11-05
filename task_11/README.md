Write a query that finds users who were active for 30 consecutive days up to and including the date 2019-07-07.

    SELECT activity_date AS "day",
    COUNT(DISTINCT user_id) AS "active_users"
    FROM activity
    WHERE activity_date > '2019-06-27' AND activity_date <= '2019-07-27'
    GROUP BY activity_date;
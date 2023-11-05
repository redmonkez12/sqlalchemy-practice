Retrieve the number of followers for each user.

    SELECT user_id, COUNT(follower_id) AS followers_count
    FROM followers
    GROUP BY user_id
    ORDER BY user_id ASC;
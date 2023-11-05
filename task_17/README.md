List the IDs of records where the temperature was higher than the previous day.

    SELECT b.weather_id AS id
    FROM weather a join weather b ON
    a.record_date = b.record_date - 1
    WHERE b.temperature > a.temperature;

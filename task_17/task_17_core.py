from sqlalchemy import Table, Column, Integer, select, Date, insert

from db import metadata


def task_17_core(engine, create_tables):
    weather = Table(
        "weather",
        metadata,
        Column("weather_id", Integer, primary_key=True),
        Column("record_date", Date, nullable=False),
        Column("temperature", Integer, nullable=False),
    )

    new_weather = [
        {"record_date": "2015-01-01", "temperature": 10},
        {"record_date": "2015-01-03", "temperature": 25},
        {"record_date": "2015-01-04", "temperature": 20},
        {"record_date": "2015-01-05", "temperature": 30},
    ]

    weather.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(weather), new_weather)
        connection.commit()

        a = weather.alias("a")
        b = weather.alias("b")

        query = (
            select(b.c.weather_id)
            .select_from(a.join(b, a.c.record_date == b.c.record_date - 1))
            .where(b.c.temperature > a.c.temperature)
        )

        result = connection.execute(query)
        print(result.all())

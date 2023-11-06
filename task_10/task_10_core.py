from sqlalchemy import Table, Column, Integer, func, select, insert

from db import metadata


def task_10_core(engine, creat_tables):
    number = Table(
        "numbers",
        metadata,
        Column("number_id", Integer, primary_key=True),
        Column("num", Integer, nullable=False),
    )

    new_numbers = [
        {"num": 8},
        {"num": 8},
        {"num": 3},
        {"num": 3},
        {"num": 1},
        {"num": 4},
        {"num": 5},
        {"num": 6},
    ]

    number.drop(engine, checkfirst=True)
    creat_tables()

    with engine.connect() as connection:
        connection.execute(insert(number), new_numbers)
        connection.commit()

        subquery = select(number.c.num).group_by(number.c.num).having(func.count(number.c.num) == 1).subquery()
        query = select(func.max(subquery.c.num).label("num"))

        result = connection.execute(query)
        print(result.all())

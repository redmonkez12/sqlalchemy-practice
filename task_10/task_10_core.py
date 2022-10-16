from sqlalchemy import Table, Column, Integer, func, select

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")

number = Table(
    "numbers",
    metadata,
    Column("number_id", Integer, primary_key=True),
    Column("num", Integer, nullable=False),
)

create_tables(engine)

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

connection.execute(number.insert(), new_numbers)

subquery = select(number.c.num).group_by(number.c.num).having(func.count(number.c.num) == 1).subquery()
query = select(func.max(subquery.c.num).label("num"))
result = connection.execute(query)

for row in result:
    print(row)

connection.close()

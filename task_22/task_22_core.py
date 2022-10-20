from sqlalchemy import Table, Column, Integer, select, func

from db import db_connect, create_tables, metadata

engine, connection = db_connect()

actor_director = Table(
    "actor_director",
    metadata,
    Column("actor_id", Integer, nullable=False),
    Column("director_id", Integer, nullable=False),
    Column("timestamp", Integer, nullable=False),
)

create_tables(engine)

new_actor_director = [
    {"actor_id": 1, "director_id": 1, "timestamp": 0},
    {"actor_id": 1, "director_id": 1, "timestamp": 1},
    {"actor_id": 1, "director_id": 1, "timestamp": 2},
    {"actor_id": 1, "director_id": 2, "timestamp": 3},
    {"actor_id": 1, "director_id": 2, "timestamp": 4},
    {"actor_id": 2, "director_id": 1, "timestamp": 5},
    {"actor_id": 2, "director_id": 1, "timestamp": 6},
]

connection.execute(actor_director.insert(), new_actor_director)

query = select(actor_director.c.actor_id, actor_director.c.director_id) \
    .group_by(actor_director.c.actor_id, actor_director.c.director_id) \
    .having(func.count() >= 3)
result = connection.execute(query)

for row in result:
    print(row)

connection.close()

from sqlalchemy import Table, Column, Integer, select, asc, func

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")


followers = Table(
    "followers",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("follower_id", Integer, primary_key=True),
)

create_tables(engine)

new_followers = [
    {"user_id": 0, "follower_id": 1},
    {"user_id": 1, "follower_id": 0},
    {"user_id": 2, "follower_id": 0},
    {"user_id": 2, "follower_id": 1},
]

connection.execute(followers.insert(), new_followers)

query = select([followers.c.user_id, func.count(followers.c.follower_id).label("followers_count")])\
    .group_by(followers.c.user_id)\
    .order_by(asc(followers.c.user_id))
result = connection.execute(query)
for row in result:
    print(row)

connection.close()

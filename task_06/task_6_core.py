from sqlalchemy import Table, Column, Integer, select, asc, func, insert

from db import metadata


def task_06_core(engine, create_tables):
    followers = Table(
        "followers",
        metadata,
        Column("user_id", Integer, primary_key=True),
        Column("follower_id", Integer, primary_key=True),
    )

    new_followers = [
        {"user_id": 0, "follower_id": 1},
        {"user_id": 1, "follower_id": 0},
        {"user_id": 2, "follower_id": 0},
        {"user_id": 2, "follower_id": 1},
    ]

    followers.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(followers), new_followers)
        connection.commit()

        query = (
            select(followers.c.user_id, func.count(followers.c.follower_id).label("followers_count"))
            .group_by(followers.c.user_id)
            .order_by(asc(followers.c.user_id))
        )

        result = connection.execute(query)
        print(result.all())

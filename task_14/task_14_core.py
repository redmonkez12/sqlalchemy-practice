from sqlalchemy import Table, Column, Integer, Text, Float, func, and_, desc, insert

from db import metadata


def task_14_core(engine, create_tables):
    movie = Table(
        "movies",
        metadata,
        Column("movie_id", Integer, primary_key=True),
        Column("movie", Text, nullable=False),
        Column("description", Text, nullable=False),
        Column("rating", Float, nullable=False),
    )

    new_movies = [
        {"movie": "War", "description": "great 3D", "rating": 8.9},
        {"movie": "Science", "description": "fiction", "rating": 8.5},
        {"movie": "Irish", "description": "boring", "rating": 6.2},
        {"movie": "Ice song", "description": "Fantasy", "rating": 8.6},
        {"movie": "House card", "description": "Interesting", "rating": 9.1},
    ]

    movie.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(movie), new_movies)
        connection.commit()

        query = (
            movie.select()
            .where(and_(func.mod(movie.c.movie_id, 2) == 1, movie.c.description != "boring"))
            .order_by(desc(movie.c.rating))
        )

        result = connection.execute(query)
        print(result.all())

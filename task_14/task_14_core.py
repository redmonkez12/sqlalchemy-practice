from sqlalchemy import Table, Column, Integer, Text, Float, func, and_, desc

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")

movie = Table(
    "movies",
    metadata,
    Column("movie_id", Integer, primary_key=True),
    Column("movie", Text, nullable=False),
    Column("description", Text, nullable=False),
    Column("rating", Float, nullable=False),
)

create_tables(engine)

new_movies = [
    {"movie": "War", "description": "great 3D", "rating": 8.9},
    {"movie": "Science", "description": "fiction", "rating": 8.5},
    {"movie": "Irish", "description": "boring", "rating": 6.2},
    {"movie": "Ice song", "description": "Fantasy", "rating": 8.6},
    {"movie": "House card", "description": "Interesting", "rating": 9.1},
]

connection.execute(movie.insert(), new_movies)

query = movie.select() \
    .where(and_(func.mod(movie.c.movie_id, 2) == 1, movie.c.description != "boring")) \
    .order_by(desc(movie.c.rating))
result = connection.execute(query)

for row in result:
    print(row)

connection.close()

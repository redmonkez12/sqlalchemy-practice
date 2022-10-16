from sqlalchemy import Column, Integer, Text, Float, and_, func, desc
from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect("postgres", "123456", "etoro")

session = create_session(engine)


class Movie(Base):
    __tablename__ = "movies"

    movie_id = Column(Integer, primary_key=True)
    movie = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    rating = Column(Float, nullable=False)


create_tables_orm(engine)

new_movies = [
    Movie(movie="War", description="great 3D", rating=8.9),
    Movie(movie="Science", description="fiction", rating=8.5),
    Movie(movie="Irish", description="boring", rating=6.2),
    Movie(movie="Ice song", description="Fantasy", rating=8.6),
    Movie(movie="House card", description="Interesting", rating=9.1),
]

session.add_all(new_movies)

result = session.query(Movie)\
    .where(and_(func.mod(Movie.movie_id, 2) == 1, Movie.description != "boring")) \
    .order_by(desc(Movie.rating))

for row in result:
    print(row.movie_id)

session.close()
connection.close()

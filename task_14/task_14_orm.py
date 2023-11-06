from sqlalchemy import Column, Integer, Text, Float, and_, func, desc
from sqlalchemy.orm import Session

from db import Base


def task_14_orm(engine, create_tables):
    class Movie(Base):
        __tablename__ = "movies"

        movie_id = Column(Integer, primary_key=True)
        movie = Column(Text, nullable=False)
        description = Column(Text, nullable=False)
        rating = Column(Float, nullable=False)

        def __repr__(self):
            return f"{self.movie}"

    new_movies = [
        Movie(movie="War", description="great 3D", rating=8.9),
        Movie(movie="Science", description="fiction", rating=8.5),
        Movie(movie="Irish", description="boring", rating=6.2),
        Movie(movie="Ice song", description="Fantasy", rating=8.6),
        Movie(movie="House card", description="Interesting", rating=9.1),
    ]

    Movie.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_movies)
        session.commit()

        result = (
            session.query(Movie)
            .where(and_(func.mod(Movie.movie_id, 2) == 1, Movie.description != "boring"))
            .order_by(desc(Movie.rating))
        )

        print(result.all())

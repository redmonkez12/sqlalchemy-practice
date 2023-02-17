from sqlalchemy import Column, Integer, func
from db import db_connect, create_session, Base, create_tables_orm
from utils import print_result

engine, connection = db_connect()

session = create_session(engine)


class ActorDirector(Base):
    __tablename__ = "actor_director"

    actor_director = Column(Integer, primary_key=True)
    actor_id = Column(Integer, nullable=False)
    director_id = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)


create_tables_orm(engine)

new_actor_director = [
    ActorDirector(actor_id=1, director_id=1, timestamp=0),
    ActorDirector(actor_id=1, director_id=1, timestamp=1),
    ActorDirector(actor_id=1, director_id=1, timestamp=2),
    ActorDirector(actor_id=1, director_id=2, timestamp=3),
    ActorDirector(actor_id=1, director_id=2, timestamp=4),
    ActorDirector(actor_id=2, director_id=1, timestamp=5),
    ActorDirector(actor_id=2, director_id=1, timestamp=6),
]

session.add_all(new_actor_director)
session.commit()

result = (
    session.query(ActorDirector.actor_id, ActorDirector.director_id)
    .group_by(ActorDirector.actor_id, ActorDirector.director_id)
    .having(func.count() >= 3)
)
print_result(result)

session.close()
connection.close()

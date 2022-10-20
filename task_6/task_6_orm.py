from sqlalchemy import Column, Integer, func, asc

from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect()

session = create_session(engine)


class Follower(Base):
    __tablename__ = "followers"

    user_id = Column(Integer, primary_key=True)
    follower_id = Column(Integer, primary_key=True)


create_tables_orm(engine)

new_followers = [
    Follower(user_id=0, follower_id=1),
    Follower(user_id=1, follower_id=0),
    Follower(user_id=2, follower_id=0),
    Follower(user_id=2, follower_id=1),
]

session.add_all(new_followers)
session.commit()

result = session.query(Follower.user_id, func.count(Follower.follower_id).label("followers_count"))\
    .group_by(Follower.user_id)\
    .order_by(asc(Follower.user_id))

for row in result:
    print(row)

session.close()
connection.close()

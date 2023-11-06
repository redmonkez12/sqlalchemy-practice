from sqlalchemy import Column, Integer, func, asc
from sqlalchemy.orm import Session

from db import Base


def task_06_orm(engine, create_tables):
    class Follower(Base):
        __tablename__ = "followers"

        user_id = Column(Integer, primary_key=True)
        follower_id = Column(Integer, primary_key=True)

    new_followers = [
        Follower(user_id=0, follower_id=1),
        Follower(user_id=1, follower_id=0),
        Follower(user_id=2, follower_id=0),
        Follower(user_id=2, follower_id=1),
    ]

    Follower.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_followers)
        session.commit()

        result = (
            session.query(Follower.user_id, func.count(Follower.follower_id).label("followers_count"))
            .group_by(Follower.user_id)
            .order_by(asc(Follower.user_id))
        )

        print(result.all())

from sqlalchemy import Column, Integer, func, Date, Text, and_, distinct
from sqlalchemy.orm import Session

from db import Base


def task_11_orm(engine, create_tables):
    class Activity(Base):
        __tablename__ = "activity"

        activity_id = Column(Integer, primary_key=True)
        user_id = Column(Integer, nullable=False)
        session_id = Column(Integer, nullable=False)
        activity_date = Column(Date, nullable=False)
        activity_type = Column(Text, nullable=False)

    new_activities = [
        Activity(user_id=1, session_id=1, activity_date="2019-07-20", activity_type="open_session"),
        Activity(user_id=1, session_id=1, activity_date="2019-07-20", activity_type="scroll_down"),
        Activity(user_id=1, session_id=1, activity_date="2019-07-20", activity_type="end_session"),
        Activity(user_id=2, session_id=4, activity_date="2019-07-20", activity_type="open_session"),
        Activity(user_id=2, session_id=4, activity_date="2019-07-21", activity_type="send_message"),
        Activity(user_id=2, session_id=4, activity_date="2019-07-21", activity_type="end_session"),
        Activity(user_id=3, session_id=2, activity_date="2019-07-21", activity_type="open_session"),
        Activity(user_id=3, session_id=2, activity_date="2019-07-21", activity_type="send_message"),
        Activity(user_id=3, session_id=2, activity_date="2019-07-21", activity_type="end_session"),
        Activity(user_id=4, session_id=3, activity_date="2019-06-25", activity_type="open_session"),
        Activity(user_id=4, session_id=3, activity_date="2019-06-25", activity_type="end_session"),
    ]

    Activity.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_activities)
        session.commit()

        result = (
            session.query(
                Activity.activity_date.label("day"),
                func.count(distinct(Activity.user_id))
            ).where(
                and_(
                    Activity.activity_date > func.date("2019-06-27"),
                    Activity.activity_date <= func.date("2019-07-27"),
                )
            )
            .group_by(Activity.activity_date)
        )

        print(result.all())

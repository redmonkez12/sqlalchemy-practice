from sqlalchemy import Table, Column, Integer, func, select, Date, Text, and_, distinct, insert

from db import db_connect, create_tables, metadata
from utils import print_result

engine, connection = db_connect()

activity = Table(
    "activity",
    metadata,
    Column("user_id", Integer, nullable=False),
    Column("session_id", Integer, nullable=False),
    Column("activity_date", Date, nullable=False),
    Column("activity_type", Text, nullable=False),
)

create_tables(engine)

new_activities = [
    {"user_id": 1, "session_id": 1, "activity_date": "2019-07-20", "activity_type": "open_session"},
    {"user_id": 1, "session_id": 1, "activity_date": "2019-07-20", "activity_type": "scroll_down"},
    {"user_id": 1, "session_id": 1, "activity_date": "2019-07-20", "activity_type": "end_session"},
    {"user_id": 2, "session_id": 4, "activity_date": "2019-07-20", "activity_type": "open_session"},
    {"user_id": 2, "session_id": 4, "activity_date": "2019-07-21", "activity_type": "send_message"},
    {"user_id": 2, "session_id": 4, "activity_date": "2019-07-21", "activity_type": "end_session"},
    {"user_id": 3, "session_id": 2, "activity_date": "2019-07-21", "activity_type": "open_session"},
    {"user_id": 3, "session_id": 2, "activity_date": "2019-07-21", "activity_type": "send_message"},
    {"user_id": 3, "session_id": 2, "activity_date": "2019-07-21", "activity_type": "end_session"},
    {"user_id": 4, "session_id": 3, "activity_date": "2019-06-25", "activity_type": "open_session"},
    {"user_id": 4, "session_id": 3, "activity_date": "2019-06-25", "activity_type": "end_session"},
]

connection.execute(insert(activity), new_activities)
connection.commit()

query = (
    select(
        activity.c.activity_date.label("day"),
        func.count(distinct(activity.c.user_id)).label("active_users")
    ).where(and_(activity.c.activity_date > "2019-06-27", activity.c.activity_date <= "2019-07-27"))
    .group_by(activity.c.activity_date)
)
result = connection.execute(query)
print_result(result)

connection.close()

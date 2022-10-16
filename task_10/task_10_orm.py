from sqlalchemy import Column, Integer, func
from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect("postgres", "123456", "etoro")

session = create_session(engine)


class Number(Base):
    __tablename__ = "numbers"

    number_id = Column(Integer, primary_key=True)
    num = Column(Integer, nullable=False)


create_tables_orm(engine)

new_numbers = [
    Number(num=8),
    Number(num=8),
    Number(num=3),
    Number(num=3),
    Number(num=1),
    Number(num=4),
    Number(num=5),
    Number(num=6),
]

session.add_all(new_numbers)
session.commit()

subquery = session.query(Number.num).group_by(Number.num).having(func.count(Number.num) == 1).subquery()
result = session.query(func.max(subquery.c.num).label("num"))

for row in result:
    print(row)

session.close()
connection.close()

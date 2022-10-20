from sqlalchemy import Column, Integer, Text, func, Date, distinct, asc
from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect()

session = create_session(engine)


class Course(Base):
    __tablename__ = "courses"

    student_id = Column(Integer, primary_key=True)
    student = Column(Text, nullable=False)
    class_ = Column(Text, nullable=False)


create_tables_orm(engine)

new_courses = [
    Course(student="A", class_="Math"),
    Course(student="B", class_="English"),
    Course(student="C", class_="Math"),
    Course(student="D", class_="Biology"),
    Course(student="E", class_="Math"),
    Course(student="F", class_="Computer"),
    Course(student="G", class_="Math"),
    Course(student="H", class_="Math"),
    Course(student="HI", class_="Math"),
]

session.add_all(new_courses)

result = session.query(Course.class_)\
    .group_by(Course.class_)\
    .having(func.count(distinct(Course.student)) >= 5)

for row in result:
    print(row)

session.close()
connection.close()

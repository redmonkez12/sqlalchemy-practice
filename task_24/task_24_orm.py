from sqlalchemy import Column, Integer, Text, func, distinct
from db import db_connect, Base, create_tables_orm
from sqlalchemy.orm import Session

engine = db_connect()


class Course(Base):
    __tablename__ = "courses"

    student_id = Column(Integer, primary_key=True)
    student = Column(Text, nullable=False)
    class_ = Column("class", Text, nullable=False)


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

with Session(engine) as session:
    session.add_all(new_courses)
    session.commit()

    result = (
        session.query(Course.class_)
        .group_by(Course.class_)
        .having(func.count(distinct(Course.student)) >= 5)
    )

    print(result.all())

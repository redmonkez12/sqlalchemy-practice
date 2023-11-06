from sqlalchemy import Column, Integer, Text, func, distinct
from sqlalchemy.orm import Session

from db import Base


def task_24_orm(engine, create_tables):
    class Course(Base):
        __tablename__ = "courses"

        student_id = Column(Integer, primary_key=True)
        student = Column(Text, nullable=False)
        class_ = Column("class", Text, nullable=False)

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

    Course.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_courses)
        session.commit()

        result = (
            session.query(Course.class_)
            .group_by(Course.class_)
            .having(func.count(distinct(Course.student)) >= 5)
        )

        print(result.all())

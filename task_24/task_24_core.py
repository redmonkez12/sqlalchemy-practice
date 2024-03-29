from sqlalchemy import Table, Column, Integer, Text, func, select, distinct, insert

from db import metadata


def task_24_core(engine, create_tables):
    course = Table(
        "courses",
        metadata,
        Column("student_id", Integer, primary_key=True),
        Column("student", Text, nullable=False),
        Column("class", Text, nullable=False),
    )

    new_courses = [
        {"student": "A", "class": "Math"},
        {"student": "B", "class": "English"},
        {"student": "C", "class": "Math"},
        {"student": "D", "class": "Biology"},
        {"student": "E", "class": "Math"},
        {"student": "F", "class": "Computer"},
        {"student": "G", "class": "Math"},
        {"student": "H", "class": "Math"},
        {"student": "I", "class": "Math"},
    ]

    course.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(course), new_courses)
        connection.commit()

        query = (
            select(course.c["class"])
            .group_by(course.c["class"])
            .having(func.count(distinct(course.c.student)) >= 5)
        )

        result = connection.execute(query)
        print(result.all())

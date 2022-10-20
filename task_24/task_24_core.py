from sqlalchemy import Table, Column, Integer, Text, Date, func, select, distinct, asc

from db import db_connect, create_tables, metadata

engine, connection = db_connect()

course = Table(
    "courses",
    metadata,
    Column("student_id", Integer, primary_key=True),
    Column("student", Text, nullable=False),
    Column("class", Text, nullable=False),
)

create_tables(engine)

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

connection.execute(course.insert(), new_courses)

query = select(course.c["class"])\
    .group_by(course.c["class"])\
    .having(func.count(distinct(course.c.student)) >= 5)

result = connection.execute(query)

for row in result:
    print(row)

connection.close()

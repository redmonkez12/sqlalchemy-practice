from sqlalchemy import Table, Column, Integer, Text, select, insert

from db import db_connect, create_tables, metadata

engine = db_connect()

department = Table(
    "departments",
    metadata,
    Column("department_id", Integer, primary_key=True),
    Column("department_name", Text, nullable=False),
)

student = Table(
    "students",
    metadata,
    Column("student_id", Integer, primary_key=True),
    Column("student_name", Text, nullable=False),
    Column("department_id", Integer, nullable=False),
)

create_tables(engine)

new_departments = [
    {"department_name": "Electrical Engineering"},
    {"department_name": "Computer Engineering"},
    {"department_name": "Business Administration"},
]

new_students = [
    {"student_name": "Alice", "department_id": 1},
    {"student_name": "Bob", "department_id": 7},
    {"student_name": "Jennifer", "department_id": 13},
    {"student_name": "Jasmine", "department_id": 14},
    {"student_name": "Steve", "department_id": 77},
    {"student_name": "Luis", "department_id": 74},
    {"student_name": "Jonathan", "department_id": 1},
    {"student_name": "Daiana", "department_id": 7},
    {"student_name": "Madelynn", "department_id": 33},
    {"student_name": "John", "department_id": 1},
]

with engine.connect() as connection:
    connection.execute(insert(department), new_departments)
    connection.execute(insert(student), new_students)
    connection.commit()

    query = (
        select(student.c.student_id, student.c.student_name)
        .where(student.c.department_id.not_in(select(department.c.department_id)))
    )

    result = connection.execute(query)
    print(result.all())

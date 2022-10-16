from sqlalchemy import Table, Column, Integer, Text, select

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")

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

connection.execute(department.insert(), new_departments)
connection.execute(student.insert(), new_students)

query = select(student.c.student_id, student.c.student_name)\
    .where(student.c.department_id.not_in(select(department.c.department_id)))
result = connection.execute(query)

for row in result:
    print(row)

connection.close()

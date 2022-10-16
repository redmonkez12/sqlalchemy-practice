from sqlalchemy import Column, Integer, Text, Float, and_, func, desc
from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect("postgres", "123456", "etoro")

session = create_session(engine)


class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True)
    department_name = Column(Text, nullable=False)


class Student(Base):
    __tablename__ = "students"

    student_id = Column(Integer, primary_key=True)
    student_name = Column(Text, nullable=False)
    department_id = Column(Integer, nullable=False)


create_tables_orm(engine)

new_departments = [
    Department(department_name="Electrical Engineering"),
    Department(department_name="Computer Engineering"),
    Department(department_name="Business Administration"),
]

new_students = [
    Student(student_name="Alice", department_id=1),
    Student(student_name="Bob", department_id=7),
    Student(student_name="Jennifer", department_id=13),
    Student(student_name="Jasmine", department_id=14),
    Student(student_name="Steve", department_id=77),
    Student(student_name="Luis", department_id=74),
    Student(student_name="Jonathan", department_id=1),
    Student(student_name="Daiana", department_id=7),
    Student(student_name="Madelynn", department_id=33),
    Student(student_name="John", department_id=1),
]

session.add_all(new_students)
session.commit()
session.add_all(new_departments)

result = session.query(Student.student_id, Student.student_name)\
    .where(Student.department_id.not_in(session.query(Department.department_id)))

for row in result:
    print(row)

session.close()
connection.close()

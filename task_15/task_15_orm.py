from sqlalchemy import Column, Integer, Text
from db import db_connect, Base, create_tables_orm
from sqlalchemy.orm import Session

engine = db_connect()

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

with Session(engine) as session:
    session.add_all(new_students)
    session.add_all(new_departments)
    session.commit()

    result = (
        session.query(Student.student_id, Student.student_name)
        .where(Student.department_id.not_in(session.query(Department.department_id)))
    )

    print(result.all())

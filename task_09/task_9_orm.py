from sqlalchemy import Column, Integer, Text, Numeric, union

from db import db_connect, Base, create_tables_orm
from sqlalchemy.orm import Session

engine = db_connect()

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


class Salary(Base):
    __tablename__ = "salaries"

    salary_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, nullable=False)
    salary = Column(Numeric, nullable=False)


create_tables_orm(engine)

new_employees = [
    Employee(employee_id=2, name="Crew"),
    Employee(employee_id=4, name="Heaven"),
    Employee(employee_id=5, name="Kristian"),
]

new_salaries = [
    Salary(employee_id=5, salary=76071),
    Salary(employee_id=1, salary=22517),
    Salary(employee_id=4, salary=63539),
]

with Session(engine) as session:
    session.add_all(new_employees)
    session.add_all(new_salaries)
    session.commit()

    query = union(
        session.query(Employee.employee_id).where(Employee.employee_id.not_in(session.query(Salary.employee_id))),
        session.query(Salary.employee_id).where(Salary.employee_id.not_in(session.query(Employee.employee_id))),
    )

    result = session.execute(query)
    print(result.all())

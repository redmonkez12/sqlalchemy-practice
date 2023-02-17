from sqlalchemy import Column, Integer, Text, Numeric, and_, asc, func
from sqlalchemy.sql.functions import coalesce
from sqlalchemy.orm import aliased

from db import db_connect, create_session, Base, create_tables_orm
from utils import print_result

engine, connection = db_connect()

session = create_session(engine)


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    salary = Column(Numeric, nullable=False)


create_tables_orm(engine)

new_employees = [
    Employee(name="Meir", salary=3000),
    Employee(name="Michael", salary=38000),
    Employee(name="Addilyn", salary=7400),
    Employee(name="Juan", salary=6100),
    Employee(name="Kannon", salary=7700),
]

session.add_all(new_employees)
session.commit()

e = aliased(Employee)
ee = aliased(Employee)

result = (
    session.query(e.employee_id, coalesce(ee.salary, 0).label("bonus"))
    .outerjoin(ee, and_(
        e.employee_id == ee.employee_id,
        func.mod(e.employee_id, 2) == 1,
        ee.name.not_like("M%")
    )
               )
    .order_by(asc(e.employee_id))
)

print_result(result)

session.close()
connection.close()

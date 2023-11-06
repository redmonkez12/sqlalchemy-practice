from sqlalchemy import Column, Integer, Text, Numeric, and_, asc, func
from sqlalchemy.orm import aliased, Session
from sqlalchemy.sql.functions import coalesce

from db import Base


def task_08_orm(engine, create_tables):
    class Employee(Base):
        __tablename__ = "employees"

        employee_id = Column(Integer, primary_key=True)
        name = Column(Text, nullable=False)
        salary = Column(Numeric, nullable=False)

    new_employees = [
        Employee(name="Meir", salary=3000),
        Employee(name="Michael", salary=38000),
        Employee(name="Addilyn", salary=7400),
        Employee(name="Juan", salary=6100),
        Employee(name="Kannon", salary=7700),
    ]

    Employee.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
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

        print(result.all())

from sqlalchemy import Column, Integer, func
from db import db_connect, Base, create_tables_orm
from sqlalchemy.orm import Session

engine = db_connect()


class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, nullable=False)


create_tables_orm(engine)

new_employees = [
    Employee(team_id=8),
    Employee(team_id=8),
    Employee(team_id=8),
    Employee(team_id=7),
    Employee(team_id=9),
    Employee(team_id=9),
]

with Session(engine) as session:
    session.add_all(new_employees)
    session.commit()

    subquery = (
        session.query(Employee.team_id.label("team_id"), func.count().label("count"))
        .group_by(Employee.team_id).subquery()
    )
    result = (
        session.query(Employee.employee_id, subquery.c.count.label("team_size"))
        .outerjoin(subquery, subquery.c.team_id == Employee.team_id)
    )

    print(result.all())

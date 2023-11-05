from sqlalchemy import Table, Column, Integer, Text, Numeric, ForeignKey, select, null, or_, insert

from db import db_connect, create_tables, metadata

engine = db_connect()

employee = Table(
    "employee",
    metadata,
    Column("employee_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("supervisor", Integer, nullable=True),
    Column("salary", Numeric, nullable=False),
)

bonus = Table(
    "bonus",
    metadata,
    Column("bonus_id", Integer, primary_key=True),
    Column("employee_id", Integer, ForeignKey(employee.c.employee_id, ondelete="CASCADE", onupdate="CASCADE"),
           nullable=False),
    Column("bonus", Numeric, nullable=True),
)

create_tables(engine)

new_employees = [
    {"employee_id": 3, "name": "Brad", "supervisor": None, "salary": 4000},
    {"employee_id": 1, "name": "John", "supervisor": 3, "salary": 1000},
    {"employee_id": 2, "name": "Dan", "supervisor": 3, "salary": 2000},
    {"employee_id": 4, "name": "Thomas", "supervisor": 3, "salary": 4000},
]

new_bonus = [
    {"employee_id": 2, "bonus": 500},
    {"employee_id": 4, "bonus": 2000},
]

with engine.connect() as connection:
    connection.execute(insert(employee), new_employees)
    connection.execute(insert(bonus), new_bonus)
    connection.commit()

    query = (
        select(employee.c.name, bonus.c.bonus)
        .select_from(employee.outerjoin(bonus, bonus.c.employee_id == employee.c.employee_id))
        .where(or_(bonus.c.bonus < 1000, bonus.c.bonus == null()))
    )
    result = connection.execute(query)
    print(result.all())

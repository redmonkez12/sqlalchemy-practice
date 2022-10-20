from sqlalchemy import Table, Column, Integer, Text, Numeric, select, and_, func, asc
from sqlalchemy.sql.functions import coalesce

from db import db_connect, create_tables, metadata

engine, connection = db_connect()

employee = Table(
    "employees",
    metadata,
    Column("employee_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("salary", Numeric, nullable=False),
)

create_tables(engine)

new_employees = [
    {"name": "Meir", "salary": 3000},
    {"name": "Michael", "salary": 38000},
    {"name": "Addilyn", "salary": 7400},
    {"name": "Juan", "salary": 6100},
    {"name": "Kannon", "salary": 7700},
]

connection.execute(employee.insert(), new_employees)

e = employee.alias("e")
ee = employee.alias("ee")

query = select(e.c.employee_id, coalesce(ee.c.salary, 0).label("bonus"))\
    .select_from(e.outerjoin(ee, and_(e.c.employee_id == ee.c.employee_id, func.mod(e.c.employee_id, 2) == 1, ee.c.name.notlike("M%"))))\
    .order_by(asc(e.c.employee_id))

result = connection.execute(query)
for row in result:
    print(row.employee_id, row.bonus)

connection.close()

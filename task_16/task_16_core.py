from sqlalchemy import Table, Column, Integer, select, func, text

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")

employee = Table(
    "employees",
    metadata,
    Column("employee_id", Integer, primary_key=True),
    Column("team_id", Integer, nullable=False),
)

create_tables(engine)

new_employees = [
    {"team_id": 8},
    {"team_id": 8},
    {"team_id": 8},
    {"team_id": 7},
    {"team_id": 9},
    {"team_id": 9},
]

connection.execute(employee.insert(), new_employees)

# subquery = select(employee.c.team_id.label("team_id"), func.count().label("count")).group_by(
#     employee.c.team_id).subquery()
# query = select(employee.c.employee_id, subquery.c.count.label("team_size")) \
#     .select_from(employee.outerjoin(subquery, subquery.c.team_id == employee.c.team_id)
#                  )

subquery = select(employee.c.team_id.label("team_id"), func.count().label("count")).group_by(
    employee.c.team_id).alias("team")
query = select(employee.c.employee_id, subquery.c.count.label("team_size")) \
    .select_from(employee.outerjoin(subquery, subquery.c.team_id == employee.c.team_idx))


result = connection.execute(query)

for row in result:
    print(row)

connection.close()

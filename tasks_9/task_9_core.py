from sqlalchemy import Table, Column, Integer, Text, Numeric, union, select, insert

from db import db_connect, create_tables, metadata
from utils import print_result

engine, connection = db_connect()

employee = Table(
    "employees",
    metadata,
    Column("employee_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
)

salary = Table(
    "salaries",
    metadata,
    Column("salary_id", Integer, primary_key=True),
    Column("employee_id", Integer, nullable=False),
    Column("salary", Numeric, nullable=False),
)

create_tables(engine)

new_employees = [
    {"employee_id": 2, "name": "Crew"},
    {"employee_id": 4, "name": "Heaven"},
    {"employee_id": 5, "name": "Kristian"},
]

new_salaries = [
    {"employee_id": 5, "salary": 76071},
    {"employee_id": 1, "salary": 22517},
    {"employee_id": 4, "salary": 63539},
]

connection.execute(insert(employee), new_employees)
connection.execute(insert(salary), new_salaries)
connection.commit()

query = union(
    select(employee.c.employee_id).where(employee.c.employee_id.not_in(select(salary.c.employee_id))),
    select(salary.c.employee_id).where(salary.c.employee_id.not_in(select(employee.c.employee_id))),
)
result = connection.execute(query)
print_result(result)

connection.close()

from sqlalchemy import Table, Column, Integer, Text, ForeignKey, func, select, insert

from db import db_connect, create_tables, metadata

engine, connection = db_connect()

employee = Table(
    "employees",
    metadata,
    Column("employee_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("experience_years", Integer, nullable=False),
)

project = Table(
    "projects",
    metadata,
    Column("project_id", Integer, primary_key=True),
    Column("employee_id", Integer, ForeignKey(employee.c.employee_id, ondelete="CASCADE", onupdate="CASCADE"),
           primary_key=True),
)

create_tables(engine)

new_employees = [
    {"name": "Khaled", "experience_years": 3},
    {"name": "Ali", "experience_years": 2},
    {"name": "John", "experience_years": 1},
    {"name": "Doe", "experience_years": 2},
]

new_projects = [
    {"project_id": 1, "employee_id": 1},
    {"project_id": 1, "employee_id": 2},
    {"project_id": 1, "employee_id": 3},
    {"project_id": 2, "employee_id": 1},
    {"project_id": 2, "employee_id": 4},
]

with engine.connect() as connection:
    connection.execute(insert(employee), new_employees)
    connection.execute(insert(project), new_projects)
    connection.commit()

    query = (
        select(
            project.c.project_id,
            func.round(func.avg(employee.c.experience_years), 2).label("average_years"),
        ).select_from(project.outerjoin(employee, project.c.employee_id == employee.c.employee_id))
        .group_by(project.c.project_id)
    )

    result = connection.execute(query)
    print(result.all())

from sqlalchemy import Table, Column, Integer, select, func, insert

from db import metadata


def task_16_core(engine, create_tables):
    employee = Table(
        "employees",
        metadata,
        Column("employee_id", Integer, primary_key=True),
        Column("team_id", Integer, nullable=False),
    )

    new_employees = [
        {"team_id": 8},
        {"team_id": 8},
        {"team_id": 8},
        {"team_id": 7},
        {"team_id": 9},
        {"team_id": 9},
    ]

    employee.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(employee), new_employees)
        connection.commit()

        subquery = (
            select(employee.c.team_id.label("team_id"), func.count().label("count"))
            .group_by(employee.c.team_id).alias("team")
        )
        query = (
            select(employee.c.employee_id, subquery.c.count.label("team_size"))
            .select_from(employee.outerjoin(subquery, subquery.c.team_id == employee.c.team_id))
        )

        result = connection.execute(query)
        print(result.all())

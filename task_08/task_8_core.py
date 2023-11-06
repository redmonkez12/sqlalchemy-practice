from sqlalchemy import Table, Column, Integer, Text, Numeric, select, and_, func, asc, insert
from sqlalchemy.sql.functions import coalesce

from db import metadata


def task_08_core(engine, create_tables):
    employee = Table(
        "employees",
        metadata,
        Column("employee_id", Integer, primary_key=True),
        Column("name", Text, nullable=False),
        Column("salary", Numeric, nullable=False),
    )

    new_employees = [
        {"name": "Meir", "salary": 3000},
        {"name": "Michael", "salary": 38000},
        {"name": "Addilyn", "salary": 7400},
        {"name": "Juan", "salary": 6100},
        {"name": "Kannon", "salary": 7700},
    ]

    employee.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(employee), new_employees)
        connection.commit()

        e = employee.alias("e")
        ee = employee.alias("ee")

        query = (
            select(e.c.employee_id, coalesce(ee.c.salary, 0).label("bonus"))
            .select_from(
                e.outerjoin(ee,
                            and_(e.c.employee_id == ee.c.employee_id,
                                 func.mod(e.c.employee_id, 2) == 1,
                                 ee.c.name.notlike("M%")
                                 )
                            )
            )
            .order_by(asc(e.c.employee_id))
        )

        result = connection.execute(query)
        print(result)

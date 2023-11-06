from sqlalchemy import Table, Column, Text, Integer, select, or_, null, insert

from db import metadata


def task_04_core(engine, create_tables):
    customer = Table(
        "customers",
        metadata,
        Column("customer_id", Integer, primary_key=True),
        Column("name", Text, nullable=False),
        Column("referee_id", Integer, nullable=True),
    )

    new_customers = [
        {"name": "Will", "referee_id": None},
        {"name": "Jane", "referee_id": None},
        {"name": "Alex", "referee_id": 2},
        {"name": "Bill", "referee_id": None},
        {"name": "Zack", "referee_id": 1},
        {"name": "Mark", "referee_id": 2},
    ]

    customer.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(customer), new_customers)
        connection.commit()

        query = select(customer.c.name).where(or_(customer.c.referee_id != 2, customer.c.referee_id == null()))
        result = connection.execute(query)
        print(result.all())

from sqlalchemy import Table, Column, Integer, func, select, desc, insert

from db import db_connect, create_tables, metadata

engine = db_connect()

order = Table(
    "orders",
    metadata,
    Column("order_id", Integer, primary_key=True),
    Column("order_number", Integer, nullable=False),
    Column("customer_number", Integer, nullable=False),
)

create_tables(engine)

new_orders = [
    {"order_number": 1, "customer_number": 1},
    {"order_number": 2, "customer_number": 2},
    {"order_number": 3, "customer_number": 3},
    {"order_number": 4, "customer_number": 3},
    {"order_number": 5, "customer_number": 3},
    {"order_number": 6, "customer_number": 3},
]

with engine.connect() as connection:
    connection.execute(insert(order), new_orders)
    connection.commit()

    query = (
        select(order.c.customer_number)
        .group_by(order.c.customer_number)
        .order_by(desc(func.count()))
        .limit(1)
    )

    result = connection.execute(query)
    print(result.all())

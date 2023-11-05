from sqlalchemy import Table, Column, Text, Integer, ForeignKey, select, null, insert

from db import db_connect, create_tables, metadata

engine = db_connect()

customer = Table(
    "customers",
    metadata,
    Column("customer_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
)

order = Table(
    "orders",
    metadata,
    Column("order_id", Integer, primary_key=True),
    Column("customer_id", Integer, ForeignKey(customer.c.customer_id, onupdate="CASCADE", ondelete="CASCADE"),
           nullable=False)
)

create_tables(engine)

new_customers = [
    {"name": "Joe"},
    {"name": "Henry"},
    {"name": "Max"},
    {"name": "Sam"},
]

new_orders = [
    {"customer_id": 3},
    {"customer_id": 1},
]

with engine.connect() as connection:
    connection.execute(insert(customer), new_customers)
    connection.execute(insert(order), new_orders)
    connection.commit()

    query = (
        select(customer.c.customer_id)
        .where(customer.c.customer_id.not_in(select(order.c.customer_id)))
    )

    result = connection.execute(query)
    print(result)

    query = (
        select(customer.c.customer_id)
        .select_from(customer.join(order, isouter=True))
        .where(order.c.customer_id == null())
    )

    result = connection.execute(query)
    print(result)

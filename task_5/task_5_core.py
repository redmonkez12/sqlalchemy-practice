from sqlalchemy import Table, Column, Text, Integer, ForeignKey, select, text

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")

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

connection.execute(customer.insert(), new_customers)
connection.execute(order.insert(), new_orders)

# query = select(customer.c.customer_id)\
#     .where(customer.c.customer_id.not_in(select(order.c.customer_id)))

query = select([customer.c.customer_id])\
    .select_from(customer.join(order, isouter=True))\
    .where(order.c.customer_id == None)

result = connection.execute(query)
for row in result:
    print(row)

connection.close()

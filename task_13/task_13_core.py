from sqlalchemy import Table, Column, Integer, func, select, desc

from db import db_connect, create_tables, metadata

engine, connection = db_connect()

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

connection.execute(order.insert(), new_orders)

# query = select(order.c.customer_number)\
#     .group_by(order.c.customer_number) \
#     .order_by(desc(func.count())) \
#     .limit(1)

# query = order.select()
query = select(order.c.order_id, order.c.customer_number)
# session.query(Order)

result = connection.execute(query)
for row in result:
    print(row.order_id, row.customer_number)

connection.close()

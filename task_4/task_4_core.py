from sqlalchemy import Table, Column, Text, Integer, select, or_, null

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")

customer = Table(
    "customers",
    metadata,
    Column("customer_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("referee_id", Integer, nullable=True),
)

create_tables(engine)

new_customers = [
    {"name": "Will", "referee_id": None},
    {"name": "Jane", "referee_id": None},
    {"name": "Alex", "referee_id": 2},
    {"name": "Bill", "referee_id": None},
    {"name": "Zack", "referee_id": 1},
    {"name": "Mark", "referee_id": 2},
]

connection.execute(customer.insert(), new_customers)

query = select([customer.c.name]).where(or_(customer.c.referee_id != 2, customer.c.referee_id == null()))
result = connection.execute(query)
for row in result:
    print(row)

connection.close()

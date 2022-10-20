from sqlalchemy import Table, Column, Integer, Numeric, ForeignKey, select, func, null, update

from db import db_connect, create_tables, metadata

engine, connection = db_connect()

visits = Table(
    "visits",
    metadata,
    Column("visit_id", Integer, primary_key=True),
    Column("customer_id", Integer, nullable=False),
)

transactions = Table(
    "transactions",
    metadata,
    Column("transaction_id", Integer, primary_key=True),
    Column("visit_id", Integer, ForeignKey(visits.c.visit_id, ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
    Column("amount", Numeric, nullable=False),
)

create_tables(engine)

new_visits = [
    {"customer_id": 23},
    {"customer_id": 9},
    {"customer_id": 30},
    {"customer_id": 54},
    {"customer_id": 96},
    {"customer_id": 54},
    {"customer_id": 54},
]

new_transactions = [
    {"transactions_id": 2, "visit_id": 5, "amount": 310},
    {"transactions_id": 3, "visit_id": 5, "amount": 300},
    {"transactions_id": 9, "visit_id": 5, "amount": 200},
    {"transactions_id": 12, "visit_id": 1, "amount": 910},
    {"transactions_id": 13, "visit_id": 2, "amount": 970},
]

connection.execute(visits.insert(), new_visits)
connection.execute(transactions.insert(), new_transactions)

query = select(visits.c.customer_id, func.count(visits.c.visit_id).label("count_no_trans")) \
    .select_from(visits.outerjoin(transactions)) \
    .where(transactions.c.transaction_id == null()) \
    .group_by(visits.c.customer_id)
result = connection.execute(query)

for row in result:
    print(row)

connection.close()

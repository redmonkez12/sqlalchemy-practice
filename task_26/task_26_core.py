from sqlalchemy import Table, Column, Integer, Text, Date, ForeignKey, Numeric, select, func, insert

from db import db_connect, create_tables, metadata

engine = db_connect()

user = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
)

transaction = Table(
    "transactions",
    metadata,
    Column("transaction_id", Integer, primary_key=True),
    Column("transacted_on", Date, nullable=False),
    Column("amount", Numeric, nullable=False),
    Column("user_id", Integer, ForeignKey(user.c.user_id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
)

create_tables(engine)

new_users = [
    {"name": "Alice"},
    {"name": "Bob"},
    {"name": "Charlie"},
]

new_transaction = [
    {"transacted_on": "2020-08-01", "amount": 7000, "user_id": 1},
    {"transacted_on": "2020-09-01", "amount": 7000, "user_id": 1},
    {"transacted_on": "2020-09-02", "amount": -3000, "user_id": 1},
    {"transacted_on": "2020-09-12", "amount": 1000, "user_id": 2},
    {"transacted_on": "2020-08-07", "amount": 6000, "user_id": 3},
    {"transacted_on": "2020-09-07", "amount": 6000, "user_id": 3},
    {"transacted_on": "2020-09-1", "amount": -4000, "user_id": 3},
]

with engine.connect() as connection:
    connection.execute(insert(user), new_users)
    connection.execute(insert(transaction), new_transaction)
    connection.commit()

    query = (
        select(user.c.name, func.sum(transaction.c.amount).label("amount"))
        .select_from(transaction.join(user, user.c.user_id == transaction.c.user_id))
        .group_by(user.c.name)
        .having(func.sum(transaction.c.amount) > 10000)
    )
    result = connection.execute(query)
    print(result.all())

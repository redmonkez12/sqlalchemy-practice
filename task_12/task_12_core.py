from sqlalchemy import Table, Column, Integer, func, select, desc, asc, ForeignKey, insert

from db import db_connect, create_tables, metadata
from utils import print_result

engine, connection = db_connect()

product = Table(
    "products",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("price", Integer, nullable=False),
)

sale = Table(
    "sales",
    metadata,
    Column("sale_id", Integer, primary_key=True),
    Column("product_id", Integer,
           ForeignKey(product.c.product_id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    Column("user_id", Integer, nullable=False),
    Column("quantity", Integer, nullable=False),
)

create_tables(engine)

new_products = [
    {"price": 10},
    {"price": 25},
    {"price": 15},
]

new_sales = [
    {"product_id": 1, "user_id": 101, "quantity": 10},
    {"product_id": 2, "user_id": 101, "quantity": 1},
    {"product_id": 3, "user_id": 102, "quantity": 3},
    {"product_id": 3, "user_id": 102, "quantity": 2},
    {"product_id": 2, "user_id": 103, "quantity": 3},
]

connection.execute(insert(product), new_products)
connection.execute(insert(sale), new_sales)
connection.commit()

query = (
    select(
        sale.c.user_id,
        func.sum(sale.c.quantity * product.c.price).label("spending"),
    ).select_from(sale.join(product, sale.c.product_id == product.c.product_id))
    .group_by(sale.c.user_id)
    .order_by(desc("spending"), asc(sale.c.user_id))
)
result = connection.execute(query)

print_result(result)

connection.close()

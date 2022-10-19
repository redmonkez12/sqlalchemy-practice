from sqlalchemy import Table, Column, Integer, Text, ForeignKey, select, Numeric, Date, func, and_, case

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")

product = Table(
    "products",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("product_name", Text, nullable=False),
    Column("unit_price", Numeric, nullable=False),
)

sale = Table(
    "sales",
    metadata,
    Column("sales_id", Integer, primary_key=True),
    Column("seller_id", Integer, nullable=False),
    Column("product_id", Integer, ForeignKey(product.c.product_id, ondelete="CASCADE", onupdate="CASCADE"),
           nullable=False),
    Column("buyer_id", Integer, nullable=False),
    Column("sale_date", Date, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("price", Numeric, nullable=False),
)

create_tables(engine)

new_products = [
    {"product_name": "S8", "unit_price": 1000},
    {"product_name": "G4", "unit_price": 800},
    {"product_name": "iPhone", "unit_price": 1400},
]

new_sales = [
    {"seller_id": 1, "product_id": 1, "buyer_id": 1, "sale_date": "2019-01-21", "quantity": 2, "price": 2000},
    {"seller_id": 1, "product_id": 2, "buyer_id": 2, "sale_date": "2019-02-17", "quantity": 1, "price": 800},
    {"seller_id": 2, "product_id": 1, "buyer_id": 3, "sale_date": "2019-06-02", "quantity": 1, "price": 800},
    {"seller_id": 3, "product_id": 3, "buyer_id": 3, "sale_date": "2019-05-13", "quantity": 2, "price": 2800},
]

connection.execute(product.insert(), new_products)
connection.execute(sale.insert(), new_sales)

query = select(sale.c.buyer_id)\
    .select_from(sale.join(product, sale.c.product_id == product.c.product_id))\
    .group_by(sale.c.buyer_id)\
    .having(and_(
        func.sum(case((product.c.product_name == "S8", 1), else_=0)) > 0,
        func.sum(case((product.c.product_name == "iPhone", 1), else_=0)) == 0
        )
    )
result = connection.execute(query)

for row in result:
    print(row)

connection.close()

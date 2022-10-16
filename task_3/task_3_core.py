from sqlalchemy import Table, Column, Text, Integer, select, and_

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")

products = Table(
    "products",
    metadata,
    Column("product_id", Integer, primary_key=True),
    Column("low_fats", Text, nullable=False),
    Column("recyclable", Text, nullable=False),
)

create_tables(engine)

new_products = [
    {"low_fats": "Y", "recyclable": "N"},
    {"low_fats": "Y", "recyclable": "Y"},
    {"low_fats": "N", "recyclable": "Y"},
    {"low_fats": "Y", "recyclable": "Y"},
    {"low_fats": "N", "recyclable": "N"},
]

connection.execute(products.insert(new_products))

query = select(products.c.product_id).where(and_(products.c.low_fats == "Y", products.c.recyclable == "Y"))
result = connection.execute(query)
for row in result:
    print(row)

connection.close()

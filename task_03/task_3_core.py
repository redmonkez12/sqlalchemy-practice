from sqlalchemy import Table, Column, Text, Integer, select, and_, insert

from db import db_connect, metadata


def task_03_core(engine, create_tables):
    products = Table(
        "products",
        metadata,
        Column("product_id", Integer, primary_key=True),
        Column("low_fats", Text, nullable=False),
        Column("recyclable", Text, nullable=False),
    )

    new_products = [
        {"low_fats": "Y", "recyclable": "N"},
        {"low_fats": "Y", "recyclable": "Y"},
        {"low_fats": "N", "recyclable": "Y"},
        {"low_fats": "Y", "recyclable": "Y"},
        {"low_fats": "N", "recyclable": "N"},
    ]

    products.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(products), new_products)
        connection.commit()

        query = select(products.c.product_id).where(and_(products.c.low_fats == "Y", products.c.recyclable == "Y"))

        result = connection.execute(query)
        print(result.all())

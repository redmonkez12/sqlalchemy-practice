from sqlalchemy import Table, Column, Integer, Text, ForeignKey, select, func, insert

from db import metadata


def task_19_core(engine, create_tables):
    product = Table(
        "products",
        metadata,
        Column("product_id", Integer, primary_key=True),
        Column("product_name", Text, nullable=False),
    )

    sale = Table(
        "sales",
        metadata,
        Column("sale_id", Integer, nullable=False, primary_key=True),
        Column("product_id", Integer, ForeignKey(product.c.product_id, ondelete="CASCADE", onupdate="CASCADE"),
               nullable=False),
        Column("year", Integer, nullable=False, primary_key=True),
        Column("quantity", Integer, nullable=False),
        Column("price", Integer, nullable=False),
    )

    new_products = [
        {"product_id": 100, "product_name": "Nokia"},
        {"product_id": 200, "product_name": "Apple"},
        {"product_id": 300, "product_name": "Samsung"},
    ]

    new_sales = [
        {"sale_id": 1, "product_id": 100, "year": 2008, "quantity": 10, "price": 5000},
        {"sale_id": 2, "product_id": 100, "year": 2009, "quantity": 12, "price": 5000},
        {"sale_id": 7, "product_id": 200, "year": 2011, "quantity": 15, "price": 9000},
    ]

    sale.drop(engine, checkfirst=True)
    product.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(product), new_products)
        connection.execute(insert(sale), new_sales)
        connection.commit()

        query = (
            select(sale.c.product_id, func.sum(sale.c.quantity).label("total_quantity"))
            .group_by(sale.c.product_id)
        )

        result = connection.execute(query)
        print(result.all())

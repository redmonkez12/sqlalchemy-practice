from sqlalchemy import Table, Column, Integer, Text, ForeignKey, select, Numeric, Date, func, and_, case, insert

from db import metadata


def task_21_core(engine, create_tables):
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

    sale.drop(engine, checkfirst=True)
    product.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(product), new_products)
        connection.execute(insert(sale), new_sales)
        connection.commit()

        query = (
            select(sale.c.buyer_id)
            .select_from(sale.join(product, sale.c.product_id == product.c.product_id))
            .group_by(sale.c.buyer_id)
            .having(and_(
                func.sum(case((product.c.product_name == "S8", 1), else_=0)) > 0,
                func.sum(case((product.c.product_name == "iPhone", 1), else_=0)) == 0
            )
            )
        )

        result = connection.execute(query)
        print(result.all())

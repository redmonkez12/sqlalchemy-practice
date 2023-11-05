from sqlalchemy import Table, Column, Integer, Text, Date, select, asc, and_, insert

from db import db_connect, create_tables, metadata

engine = db_connect()

sale = Table(
    "sales",
    metadata,
    Column("sale_id", Integer, primary_key=True),
    Column("sale_date", Date, nullable=False),
    Column("fruit", Text, nullable=False),
    Column("sold_num", Integer, nullable=False)
)

create_tables(engine)

new_sales = [
    {"sale_date": "2020-05-01", "fruit": "apples", "sold_num": 10},
    {"sale_date": "2020-05-01", "fruit": "oranges", "sold_num": 8},
    {"sale_date": "2020-05-02", "fruit": "apples", "sold_num": 15},
    {"sale_date": "2020-05-02", "fruit": "oranges", "sold_num": 15},
    {"sale_date": "2020-05-03", "fruit": "apples", "sold_num": 20},
    {"sale_date": "2020-05-03", "fruit": "oranges", "sold_num": 0},
    {"sale_date": "2020-05-04", "fruit": "apples", "sold_num": 15},
    {"sale_date": "2020-05-04", "fruit": "oranges", "sold_num": 16},
]

with engine.connect() as connection:
    connection.execute(insert(sale), new_sales)
    connection.commit()

    a = sale.alias("a")
    b = sale.alias("b")

    query = (
        select(a.c.sale_date, (b.c.sold_num - a.c.sold_num).label("diff"))
        .select_from(a.join(b, and_(a.c.sale_date == b.c.sale_date, a.c.fruit != b.c.fruit)))
        .where(b.c.fruit == "apples")
        .order_by(asc(a.c.sale_date))
    )
    result = connection.execute(query)
    print(result.all())

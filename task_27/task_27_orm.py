from sqlalchemy import Column, Integer, Text, Date, asc, and_
from sqlalchemy.orm import aliased, Session
from db import db_connect, Base, create_tables_orm

engine = db_connect()


class Sales(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, primary_key=True)
    sale_date = Column(Date, nullable=False)
    fruit = Column(Text, nullable=False)
    sold_num = Column(Integer, nullable=False)


create_tables_orm(engine)

new_sales = [
    Sales(sale_date="2020-05-01", fruit="apples", sold_num=10),
    Sales(sale_date="2020-05-01", fruit="oranges", sold_num=8),
    Sales(sale_date="2020-05-02", fruit="apples", sold_num=15),
    Sales(sale_date="2020-05-02", fruit="oranges", sold_num=15),
    Sales(sale_date="2020-05-03", fruit="apples", sold_num=20),
    Sales(sale_date="2020-05-03", fruit="oranges", sold_num=8),
    Sales(sale_date="2020-05-04", fruit="apples", sold_num=15),
    Sales(sale_date="2020-05-04", fruit="oranges", sold_num=16),
]

with Session(engine) as session:
    session.add_all(new_sales)
    session.commit()

    a = aliased(Sales, name="a")
    b = aliased(Sales, name="b")

    result = (
        session.query(a.sale_date, (b.sold_num - a.sold_num).label("diff"))
        .join(b, and_(a.sale_date == b.sale_date, a.fruit != b.fruit))
        .where(b.fruit == "apples")
        .order_by(asc(a.sale_date))
    )

    print(result.all())

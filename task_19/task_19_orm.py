from sqlalchemy import Column, Integer, ForeignKey, func, Text
from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect("postgres", "123456", "etoro")

session = create_session(engine)


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(Text, nullable=False)


class Sale(Base):
    __tablename__ = "sales"

    sale_id = Column(Integer, nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.product_id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    year = Column(Integer, nullable=False, primary_key=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)


create_tables_orm(engine)

new_products = [
    Product(product_id=100, product_name="Nokia"),
    Product(product_id=200, product_name="Apple"),
    Product(product_id=300, product_name="Samsung"),
]

new_sales = [
    Sale(sale_id=1, product_id=100, year=2008, quantity=10, price=5000),
    Sale(sale_id=2, product_id=100, year=2009, quantity=12, price=5000),
    Sale(sale_id=7, product_id=200, year=2011, quantity=15, price=9000),
]

session.add_all(new_products)
session.add_all(new_sales)
session.commit()

result = session.query(Sale.product_id, func.sum(Sale.quantity).label("total_quantity"))\
    .group_by(Sale.product_id)
for row in result:
    print(row)

session.close()
connection.close()

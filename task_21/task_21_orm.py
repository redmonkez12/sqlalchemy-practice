from sqlalchemy import Column, Integer, Text, ForeignKey, func, Numeric, case, Date, and_
from db import db_connect, create_session, Base, create_tables_orm
from utils import print_result

engine, connection = db_connect()


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(Text, nullable=False)
    unit_price = Column(Numeric, nullable=False)


class Sale(Base):
    __tablename__ = "sales"

    sales_id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, nullable=False)
    product_id = Column(Integer, ForeignKey(Product.product_id, ondelete="CASCADE", onupdate="CASCADE"),
                        nullable=False)
    buyer_id = Column(Integer, nullable=False)
    sale_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric, nullable=False)


session = create_session(engine)

create_tables_orm(engine)

new_products = [
    Product(product_name="S8", unit_price=1000),
    Product(product_name="G4", unit_price=800),
    Product(product_name="iPhone", unit_price=1400),
]

new_sales = [
    Sale(seller_id=1, product_id=1, buyer_id=1, sale_date="2019-01-21", quantity=2, price=2000),
    Sale(seller_id=1, product_id=2, buyer_id=2, sale_date="2019-02-17", quantity=2, price=800),
    Sale(seller_id=2, product_id=1, buyer_id=3, sale_date="2019-06-02", quantity=2, price=800),
    Sale(seller_id=3, product_id=3, buyer_id=3, sale_date="2019-05-13", quantity=2, price=2000),
]

session.add_all(new_products)
session.add_all(new_sales)
session.commit()

result = (
    session.query(Sale.buyer_id)
    .join(Product, Sale.product_id == Product.product_id)
    .group_by(Sale.buyer_id)
    .having(and_(
        func.sum(case((Product.product_name == "S8", 1), else_=0)) > 0,
        func.sum(case((Product.product_name == "iPhone", 1), else_=0)) == 0
    )
    )
)
print_result(result)

session.close()
connection.close()

from sqlalchemy import Column, Integer, ForeignKey, func, asc, desc
from sqlalchemy.orm import Session

from db import Base


def task_12_orm(engine, create_tables):
    class Product(Base):
        __tablename__ = "products"

        product_id = Column(Integer, primary_key=True)
        price = Column(Integer, nullable=False)

    class Sale(Base):
        __tablename__ = "sales"

        sale_id = Column(Integer, primary_key=True)
        product_id = Column(Integer,
                            ForeignKey(Product.product_id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
        user_id = Column(Integer, nullable=False)
        quantity = Column(Integer, nullable=False)

    new_products = [
        Product(price=10),
        Product(price=25),
        Product(price=15),
    ]

    new_sales = [
        Sale(product_id=1, user_id=101, quantity=10),
        Sale(product_id=2, user_id=101, quantity=1),
        Sale(product_id=3, user_id=102, quantity=3),
        Sale(product_id=3, user_id=102, quantity=2),
        Sale(product_id=2, user_id=103, quantity=3),
    ]

    Sale.__table__.drop(engine, checkfirst=True)
    Product.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_products)
        session.add_all(new_sales)
        session.commit()

        result = (
            session.query(
                Sale.user_id,
                func.sum(Sale.quantity * Product.price).label("spending"),
            ).join(Product)
            .group_by(Sale.user_id)
            .order_by(desc("spending"), asc(Sale.user_id))
        )

        print(result.all())

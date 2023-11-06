from sqlalchemy import Column, Integer, func, desc
from sqlalchemy.orm import Session

from db import Base


def task_13_orm(engine, create_tables):
    class Order(Base):
        __tablename__ = "orders"

        order_id = Column(Integer, primary_key=True)
        order_number = Column(Integer, nullable=False)
        customer_number = Column(Integer, nullable=False)

    new_orders = [
        Order(order_number=1, customer_number=1),
        Order(order_number=2, customer_number=2),
        Order(order_number=3, customer_number=3),
        Order(order_number=4, customer_number=3),
        Order(order_number=5, customer_number=3),
        Order(order_number=6, customer_number=3),
    ]

    Order.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_orders)
        session.commit()

        result = (
            session.query(Order.customer_number)
            .group_by(Order.customer_number)
            .order_by(desc(func.count()))
            .limit(1)
        )

        print(result.all())

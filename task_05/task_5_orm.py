from sqlalchemy import Column, Integer, Text, ForeignKey

from db import db_connect, Base, create_tables_orm
from sqlalchemy.orm import Session

engine = db_connect()


class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey(Customer.customer_id, onupdate="CASCADE", ondelete="CASCADE"))


create_tables_orm(engine)

new_customers = [
    Customer(name="Joe"),
    Customer(name="Henry"),
    Customer(name="Max"),
    Customer(name="Sam"),
]

new_orders = [
    Order(customer_id=3),
    Order(customer_id=1),
]

with Session(engine) as session:
    session.add_all(new_customers)
    session.add_all(new_orders)
    session.commit()

    result = (
        session.query(Customer.customer_id)
        .where(Customer.customer_id.not_in(session.query(Order.customer_id)))
    )

    print(result.all())

    result = (
        session.query(Customer.customer_id)
        .outerjoin(Order).filter(Order.customer_id == None)
        # .outerjoin(Order).filter_by(customer_id=None)
    )

    print(result.all())

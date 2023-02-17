from sqlalchemy import Column, Integer, func, desc, select
from db import db_connect, create_session, Base, create_tables_orm
from utils import print_result

engine, connection = db_connect()

session = create_session(engine)


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True)
    order_number = Column(Integer, nullable=False)
    customer_number = Column(Integer, nullable=False)


create_tables_orm(engine)

new_orders = [
    Order(order_number=1, customer_number=1),
    Order(order_number=2, customer_number=2),
    Order(order_number=3, customer_number=3),
    Order(order_number=4, customer_number=3),
    Order(order_number=5, customer_number=3),
    Order(order_number=6, customer_number=3),
]

session.add_all(new_orders)
session.commit()

result = (
    session.query(Order.customer_number)
    .group_by(Order.customer_number)
    .order_by(desc(func.count()))
    .limit(1)
)
print_result(result)

session.close()
connection.close()

from sqlalchemy import Column, Integer, Text, ForeignKey

from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect("postgres", "123456", "etoro")

session = create_session(engine)


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

session.add_all(new_customers)
session.add_all(new_orders)
session.commit()

# result = session.query(Customer.customer_id)\
#     .filter(Customer.customer_id.not_in(session.query(Order.customer_id)))

result = session.query(Customer.customer_id)\
    .outerjoin(Order).filter(Order.customer_id == None)

for row in result:
    print(row)

session.close()
connection.close()

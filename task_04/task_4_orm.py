from sqlalchemy import Column, Integer, Text, or_, null
from sqlalchemy.orm import Session

from db import Base


def task_04_orm(engine, create_tables):
    class Customer(Base):
        __tablename__ = "customers"

        customer_id = Column(Integer, primary_key=True)
        name = Column(Text, nullable=False)
        referee_id = Column(Integer, nullable=True)

    new_customers = [
        Customer(name="Will", referee_id=None),
        Customer(name="Jane", referee_id=None),
        Customer(name="Alex", referee_id=2),
        Customer(name="Bill", referee_id=None),
        Customer(name="Zack", referee_id=1),
        Customer(name="Mark", referee_id=2),
    ]

    Customer.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_customers)
        session.commit()

        result = (
            session.query(Customer.name)
            .where(or_(Customer.referee_id != 2, Customer.referee_id == null()))
        )

        print((result.all()))

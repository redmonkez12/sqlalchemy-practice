from sqlalchemy import Column, Integer, Text, Numeric, Date, ForeignKey, select
from sqlalchemy.orm import Session

from db import Base


def task_01_orm(engine, create_tables):
    class SalesPerson(Base):
        __tablename__ = "sales_persons"

        sales_id = Column(Integer, primary_key=True)
        name = Column(Text, nullable=False)
        salary = Column(Numeric, nullable=False)
        commission_rate = Column(Integer, nullable=False)
        hire_date = Column(Date, nullable=False)

    class Company(Base):
        __tablename__ = "companies"

        company_id = Column(Integer, primary_key=True)
        name = Column(Text, nullable=False)
        city = Column(Text, nullable=False)

    class Orders(Base):
        __tablename__ = "orders"

        order_id = Column(Integer, primary_key=True)
        order_date = Column(Date, nullable=False)
        amount = Column(Numeric, nullable=False)
        company_id = Column(Integer, ForeignKey(Company.company_id, ondelete="CASCADE", onupdate="CASCADE"),
                            nullable=False)
        sales_id = Column(Integer, ForeignKey(SalesPerson.sales_id, ondelete="CASCADE", onupdate="CASCADE"),
                          nullable=False)

    new_sales_people = [
        SalesPerson(name="John", salary=100000, commission_rate=6, hire_date="2006-04-01"),
        SalesPerson(name="Amy", salary=12000, commission_rate=5, hire_date="2010-05-01"),
        SalesPerson(name="Mark", salary=65000, commission_rate=12, hire_date="2008-12-25"),
        SalesPerson(name="Pam", salary=25000, commission_rate=25, hire_date="2005-01-01"),
        SalesPerson(name="Alex", salary=5000, commission_rate=10, hire_date="2007-03-02"),
    ]

    new_companies = [
        Company(name="RED", city="Boston"),
        Company(name="ORANGE", city="New York"),
        Company(name="YELLOW", city="Boston"),
        Company(name="GREEN", city="Austin"),
    ]

    new_orders = [
        Orders(order_date="2014-01-01", company_id=3, sales_id=4, amount=10000),
        Orders(order_date="2014-02-01", company_id=4, sales_id=5, amount=10000),
        Orders(order_date="2014-03-01", company_id=1, sales_id=1, amount=10000),
        Orders(order_date="2014-04-01", company_id=1, sales_id=4, amount=10000),
    ]

    Orders.__table__.drop(engine, checkfirst=True)
    Company.__table__.drop(engine, checkfirst=True)
    SalesPerson.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_sales_people)
        session.commit()
        session.add_all(new_companies)
        session.commit()
        session.add_all(new_orders)
        session.commit()

        result = (
            session.query(SalesPerson.name)
            .where(SalesPerson.sales_id.not_in(
                select(Orders.sales_id).join(Company).where(Company.name == "RED")
            )
            )
        )

        print(result.all())

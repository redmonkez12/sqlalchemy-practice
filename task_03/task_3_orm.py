from sqlalchemy import Column, Integer, Text, and_
from sqlalchemy.orm import Session

from db import Base


def task_03_orm(engine, create_tables):
    class Products(Base):
        __tablename__ = "products"

        product_id = Column(Integer, primary_key=True)
        low_fats = Column(Text, nullable=False)
        recyclable = Column(Text, nullable=False)

    new_products = [
        Products(low_fats="Y", recyclable="N"),
        Products(low_fats="Y", recyclable="Y"),
        Products(low_fats="N", recyclable="Y"),
        Products(low_fats="Y", recyclable="Y"),
        Products(low_fats="N", recyclable="N"),
    ]

    Products.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_products)
        session.commit()

        result = (
            session.query(Products.product_id)
            .where(and_(Products.low_fats == "Y", Products.recyclable == "Y"))
        )

        print(result.all())

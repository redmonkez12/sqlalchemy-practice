from sqlalchemy import Column, Integer, Text, and_

from db import db_connect, Base, create_tables_orm
from sqlalchemy.orm import Session

engine = db_connect()

class Products(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True)
    low_fats = Column(Text, nullable=False)
    recyclable = Column(Text, nullable=False)


create_tables_orm(engine)

new_products = [
    Products(low_fats="Y", recyclable="N"),
    Products(low_fats="Y", recyclable="Y"),
    Products(low_fats="N", recyclable="Y"),
    Products(low_fats="Y", recyclable="Y"),
    Products(low_fats="N", recyclable="N"),
]

with Session(engine) as session:
    session.add_all(new_products)
    session.commit()

    result = (
        session.query(Products.product_id)
        .where(and_(Products.low_fats == "Y", Products.recyclable == "Y"))
    )

    print(result.all())

from sqlalchemy import Column, Integer, Text, and_

from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect("postgres", "123456", "etoro")

session = create_session(engine)


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

session.add_all(new_products)
session.commit()

result = session.query(Products.product_id).filter(and_(Products.low_fats == "Y", Products.recyclable == "Y"))

for row in result:
    print(row)

session.close()
connection.close()

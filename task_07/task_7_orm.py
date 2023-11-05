from sqlalchemy import Column, Integer, ForeignKey, Numeric, func, null

from db import db_connect, Base, create_tables_orm
from sqlalchemy.orm import Session

engine = db_connect()

class Visit(Base):
    __tablename__ = "visits"

    visit_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True)
    visit_id = Column(Integer, ForeignKey(Visit.visit_id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric, nullable=False)


create_tables_orm(engine)

new_visits = [
    Visit(customer_id=23),
    Visit(customer_id=9),
    Visit(customer_id=30),
    Visit(customer_id=54),
    Visit(customer_id=96),
    Visit(customer_id=54),
    Visit(customer_id=54),
]

new_transactions = [
    Transaction(transaction_id=2, visit_id=5, amount=310),
    Transaction(transaction_id=3, visit_id=5, amount=300),
    Transaction(transaction_id=9, visit_id=5, amount=200),
    Transaction(transaction_id=12, visit_id=1, amount=910),
    Transaction(transaction_id=13, visit_id=2, amount=970),
]

with Session(engine) as session:
    session.add_all(new_visits)
    session.add_all(new_transactions)
    session.commit()

    result = (
        session.query(Visit.customer_id, func.count(Visit.visit_id).label("count_no_trans"))
        .outerjoin(Transaction)
        .where(Transaction.transaction_id == null())
        .group_by(Visit.customer_id)
    )
    print(result.all())

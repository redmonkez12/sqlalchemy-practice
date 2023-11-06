from sqlalchemy import Column, Integer, Text, Date, ForeignKey, Numeric, func
from sqlalchemy.orm import Session

from db import Base


def task_26_orm(engine, create_tables):
    class User(Base):
        __tablename__ = "users"

        user_id = Column(Integer, primary_key=True)
        name = Column(Text, nullable=False)

    class Transaction(Base):
        __tablename__ = "transactions"

        transaction_id = Column(Integer, primary_key=True)
        transacted_on = Column(Date, nullable=False)
        amount = Column(Numeric, nullable=False)
        user_id = Column(Integer, ForeignKey(User.user_id, onupdate="CASCADE", ondelete="CASCADE"), nullable=False)

    new_users = [
        User(name="Alice"),
        User(name="Bob"),
        User(name="Charlie"),
    ]

    new_transaction = [
        Transaction(transacted_on="2020-08-01", amount=7000, user_id=1),
        Transaction(transacted_on="2020-09-01", amount=7000, user_id=1),
        Transaction(transacted_on="2020-09-02", amount=-3000, user_id=1),
        Transaction(transacted_on="2020-08-12", amount=1000, user_id=2),
        Transaction(transacted_on="2020-08-07", amount=6000, user_id=3),
        Transaction(transacted_on="2020-09-07", amount=6000, user_id=3),
        Transaction(transacted_on="2020-09-01", amount=-4000, user_id=3),
    ]

    Transaction.__table__.drop(engine, checkfirst=True)
    User.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_users)
        session.commit()
        session.add_all(new_transaction)
        session.commit()

        result = (
            session.query(User.name, func.sum(Transaction.amount).label("amount"))
            .select_from(Transaction)
            .join(User, User.user_id == Transaction.user_id)
            .group_by(User.name)
            .having(func.sum(Transaction.amount) > 10000)
        )

        print(result.all())

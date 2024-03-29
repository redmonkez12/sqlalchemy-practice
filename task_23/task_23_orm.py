from sqlalchemy import Column, Integer, Text, func, Date, distinct, asc
from sqlalchemy.orm import Session

from db import Base


def task_23_orm(engine, create_tables):
    class Account(Base):
        __tablename__ = "accounts"

        id = Column(Integer, primary_key=True)
        name = Column(Text, nullable=False)

    class Login(Base):
        __tablename__ = "logins"

        login_id = Column(Integer, primary_key=True)
        id = Column(Integer, nullable=False)
        login_date = Column(Date, nullable=False)

    new_accounts = [
        Account(id=1, name="Winston"),
        Account(id=7, name="Jonathan"),
    ]

    new_logins = [
        Login(id=7, login_date="2020-05-30"),
        Login(id=1, login_date="2020-05-30"),
        Login(id=7, login_date="2020-05-31"),
        Login(id=7, login_date="2020-06-01"),
        Login(id=7, login_date="2020-06-02"),
        Login(id=7, login_date="2020-06-02"),
        Login(id=7, login_date="2020-06-03"),
        Login(id=7, login_date="2020-06-07"),
        Login(id=1, login_date="2020-06-10"),
    ]

    Account.__table__.drop(engine, checkfirst=True)
    Login.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_accounts)
        session.add_all(new_logins)
        session.commit()

        cte1 = session.query(distinct(Login.id).label("id"), Login.login_date).cte("t")
        cte2 = session.query(
            cte1.c.id, (cte1.c.login_date - func.lag(cte1.c.login_date, 4)
                        .over(partition_by=cte1.c.id, order_by=cte1.c.login_date)).label("count")
        ).cte("t1")
        result = (
            session.query(distinct(cte2.c.id).label("id"), Account.name)
            .select_from(cte2.join(Account, Account.id == cte2.c.id))
            .where(cte2.c.count == 4)
            .order_by(asc(cte2.c.id))
        )

        print(result.all())

from sqlalchemy import Table, Column, Integer, Text, Date, func, select, distinct, asc, insert

from db import metadata


def task_23_core(engine, create_tables):
    account = Table(
        "accounts",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", Text, nullable=False),
    )

    login = Table(
        "logins",
        metadata,
        Column("login_id", Integer, primary_key=True),
        Column("id", Integer, nullable=False),
        Column("login_date", Date, nullable=False),
    )

    new_accounts = [
        {"id": 1, "name": "Winston"},
        {"id": 7, "name": "Jonathan"},
    ]

    new_logins = [
        {"id": 7, "login_date": "2020-05-30"},
        {"id": 1, "login_date": "2020-05-30"},
        {"id": 7, "login_date": "2020-05-31"},
        {"id": 7, "login_date": "2020-06-01"},
        {"id": 7, "login_date": "2020-06-02"},
        {"id": 7, "login_date": "2020-06-02"},
        {"id": 7, "login_date": "2020-06-03"},
        {"id": 7, "login_date": "2020-06-07"},
        {"id": 1, "login_date": "2020-06-10"},
    ]

    account.drop(engine, checkfirst=True)
    login.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(account), new_accounts)
        connection.execute(insert(login), new_logins)
        connection.commit()

        cte1 = select(distinct(login.c.id).label("id"), login.c.login_date).cte("t")
        cte2 = select(
            cte1.c.id, (cte1.c.login_date - func.lag(cte1.c.login_date, 4)
                        .over(partition_by=cte1.c.id, order_by=cte1.c.login_date)).label("count")
        ).cte("t1")
        query = (
            select(distinct(cte2.c.id).label("id"), account.c.name)
            .select_from(cte2.join(account, account.c.id == cte2.c.id))
            .where(cte2.c.count == 4)
            .order_by(asc(cte2.c.id))
        )

        result = connection.execute(query)
        print(result.all())

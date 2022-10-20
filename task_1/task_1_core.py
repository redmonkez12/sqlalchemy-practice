from sqlalchemy import (
    Table, Column, Text, Integer, Numeric, Date, select, ForeignKey, Index, UniqueConstraint)

from db import db_connect, create_tables, metadata

engine, connection = db_connect()

sales_person = Table(
    "sales_person",
    metadata,
    Column("sales_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("salary", Numeric, nullable=False),
    Column("commission_rate", Integer, nullable=False),
    Column("hire_date", Date, nullable=False),
    UniqueConstraint("name", "salary", name="udx_1"),
)

company = Table(
    "company",
    metadata,
    Column("company_id", Integer, primary_key=True),
    Column("name", Text, nullable=False),
    Column("city", Text, nullable=False),
)

order = Table(
    "orders",
    metadata,
    Column("order_id", Integer, primary_key=True),
    Column("order_date", Date, nullable=False),
    Column("amount", Numeric, nullable=False),
    Column("company_id", Integer, ForeignKey(company.c.company_id, ondelete="CASCADE", onupdate="CASCADE"),
           nullable=False),
    Column("sales_id", Integer, ForeignKey(sales_person.c.sales_id, ondelete="CASCADE", onupdate="CASCADE"),
           nullable=False),
)

create_tables(engine)

new_sales_people = [
    {"name": "John", "salary": 100000, "commission_rate": 6, "hire_date": "2006-04-01"},
    {"name": "Amy", "salary": 12000, "commission_rate": 5, "hire_date": "2010-05-01"},
    {"name": "Mark", "salary": 65000, "commission_rate": 12, "hire_date": "2008-12-25"},
    {"name": "Pam", "salary": 25000, "commission_rate": 25, "hire_date": "2005-01-01"},
    {"name": "Alex", "salary": 5000, "commission_rate": 10, "hire_date": "2007-03-02"},
]

new_companies = [
    {"name": "RED", "city": "Boston"},
    {"name": "ORANGE", "city": "New York"},
    {"name": "YELLOW", "city": "Boston"},
    {"name": "GREEN", "city": "Austin"},
]

new_orders = [
    {"order_date": "2014-01-01", "company_id": 3, "sales_id": 4, "amount": 10000},
    {"order_date": "2014-01-01", "company_id": 4, "sales_id": 5, "amount": 5000},
    {"order_date": "2014-01-01", "company_id": 1, "sales_id": 1, "amount": 50000},
    {"order_date": "2014-01-01", "company_id": 1, "sales_id": 4, "amount": 25000},
]

connection.execute(sales_person.insert(), new_sales_people)
connection.execute(company.insert(), new_companies)
connection.execute(order.insert(), new_orders)

query = select(sales_person.c.name)\
    .where(
    sales_person.c.sales_id.not_in(
        select([order.c.sales_id]).select_from(order.join(company)).where(company.c.name == "RED")
    )
)
result = connection.execute(query)
for row in result:
    print(row)

connection.close()

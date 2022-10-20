from sqlalchemy import Column, Integer, Text, Numeric, ForeignKey, select, or_, null
from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect()

session = create_session(engine)


class Employee(Base):
    __tablename__ = "employee"

    employee_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    supervisor = Column(Integer, nullable=True)
    salary = Column(Numeric, nullable=False)


class Bonus(Base):
    __tablename__ = "bonus"

    bonus_id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey(Employee.employee_id, ondelete="CASCADE", onupdate="CASCADE"),
                         nullable=False)
    bonus = Column(Numeric, nullable=True)


create_tables_orm(engine)

new_employees = [
    Employee(employee_id=3, name="Brad", supervisor=None, salary=4000),
    Employee(employee_id=1, name="John", supervisor=3, salary=1000),
    Employee(employee_id=2, name="Dan", supervisor=3, salary=2000),
    Employee(employee_id=4, name="Thomas", supervisor=3, salary=4000),
]

new_bonus = [
    Bonus(employee_id=2, bonus_id=500),
    Bonus(employee_id=4, bonus_id=2000),
]

session.add_all(new_employees)
session.commit()
session.add_all(new_bonus)
session.commit()

result = session.query(Employee.name, Bonus.bonus) \
    .select_from(Employee) \
    .outerjoin(Bonus, Bonus.employee_id == Employee.employee_id) \
    .where(or_(Bonus.bonus < 1000, Bonus.bonus == null()))

for row in result:
    print(row)

session.close()
connection.close()

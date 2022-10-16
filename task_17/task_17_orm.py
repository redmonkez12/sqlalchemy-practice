from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import aliased
from db import db_connect, create_session, Base, create_tables_orm

engine, connection = db_connect("postgres", "123456", "etoro")

session = create_session(engine)


class Weather(Base):
    __tablename__ = "weather"

    weather_id = Column(Integer, primary_key=True)
    record_date = Column(Date, nullable=False)
    temperature = Column(Integer, nullable=False)


create_tables_orm(engine)

new_weather = [
    Weather(record_date="2015-01-01", temperature=10),
    Weather(record_date="2015-01-03", temperature=25),
    Weather(record_date="2015-01-04", temperature=20),
    Weather(record_date="2015-01-05", temperature=30),
]

session.add_all(new_weather)

a = aliased(Weather)
b = aliased(Weather)

result = session.query(b.weather_id)\
    .select_from(a) \
    .join(b, a.record_date == b.record_date - 1) \
    .where(b.temperature > a.temperature)

for row in result:
    print(row)

session.close()
connection.close()

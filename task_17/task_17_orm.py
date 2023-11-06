from sqlalchemy import Column, Integer, Date
from sqlalchemy.orm import aliased, Session

from db import Base


def task_17_orm(engine, create_tables):
    class Weather(Base):
        __tablename__ = "weather"

        weather_id = Column(Integer, primary_key=True)
        record_date = Column(Date, nullable=False)
        temperature = Column(Integer, nullable=False)

    new_weather = [
        Weather(record_date="2015-01-01", temperature=10),
        Weather(record_date="2015-01-03", temperature=25),
        Weather(record_date="2015-01-04", temperature=20),
        Weather(record_date="2015-01-05", temperature=30),
    ]

    Weather.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_weather)
        session.commit()

        a = aliased(Weather)
        b = aliased(Weather)

        result = (
            session.query(b.weather_id)
            .select_from(a)
            .join(b, a.record_date == b.record_date - 1)
            .where(b.temperature > a.temperature)
        )

        print(result.all())

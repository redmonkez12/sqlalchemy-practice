from sqlalchemy import Column, Integer, BigInteger, Text, union, select, or_
from sqlalchemy.orm import Session

from db import db_connect, Base, create_tables_orm

engine = db_connect()


class Country(Base):
    __tablename__ = "countries"

    country_id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    continent = Column(Text, nullable=False)
    area = Column(Integer, nullable=False)
    population = Column(BigInteger, nullable=False)
    gdp = Column(BigInteger, nullable=False)


create_tables_orm(engine)

new_countries = [
    Country(name="Afghanistan", continent="Asia", area=652230, population=25500100, gdp=20343000000),
    Country(name="Albania", continent="Europe", area=28748, population=2831741, gdp=12960000000),
    Country(name="Algeria", continent="Africa", area=2381741, population=37100000, gdp=188681000000),
    Country(name="Andorra", continent="Europe", area=468, population=78115, gdp=3712000000),
    Country(name="Angola", continent="Africa", area=1246700, population=20609294, gdp=100990000000),
]

with Session(engine) as session:
    session.add_all(new_countries)
    session.commit()

    result = session.query(Country).filter(or_(Country.population >= 25000000, Country.area >= 3000000))

    print(result.all())

    query = union(
        select(Country.name, Country.continent, Country.area).where(Country.population >= 25000000),
        select(Country.name, Country.continent, Country.area).where(Country.area >= 3000000)
    )


    result = session.execute(query)

    print(result.all())

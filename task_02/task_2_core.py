from sqlalchemy import Table, Column, Text, Integer, BigInteger, select, or_, union, insert

from db import metadata


def task_02_core(engine, create_tables):
    country = Table(
        "countries",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", Text, nullable=False),
        Column("continent", Text, nullable=False),
        Column("area", Integer, nullable=False),
        Column("population", Integer, nullable=False),
        Column("gdp", BigInteger, nullable=False),
    )

    new_countries = [
        {"name": "Afghanistan", "continent": "Asia", "area": 652230, "population": 25500100, "gdp": 20343000000},
        {"name": "Albania", "continent": "Europe", "area": 28748, "population": 2831741, "gdp": 12960000000},
        {"name": "Algeria", "continent": "Africa", "area": 2381741, "population": 37100000, "gdp": 188681000000},
        {"name": "Andorra", "continent": "Europe", "area": 468, "population": 78115, "gdp": 3712000000},
        {"name": "Angola", "continent": "Africa", "area": 1246700, "population": 20609294, "gdp": 100990000000},
    ]

    country.drop(engine, checkfirst=True)
    create_tables()

    with engine.connect() as connection:
        connection.execute(insert(country), new_countries)
        connection.commit()

        countries = (
            select(country.c.name, country.c.continent, country.c.area)
            .where(or_(country.c.population >= 25000000, country.c.area >= 3000000))
        )

        result = connection.execute(countries)
        print(result.all())

        countries = union(
            select(country.c.name, country.c.continent, country.c.area).where(country.c.population >= 25000000),
            select(country.c.name, country.c.continent, country.c.area).where(country.c.area >= 3000000)
        )

        result = connection.execute(countries)
        print(result.all())

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from dotenv import dotenv_values

metadata = MetaData()
Base = declarative_base()


def db_connect():
    config = dotenv_values("./.env")
    username = config.get("DB_USERNAME")
    password = config.get("DB_PASSWORD")
    name = config.get("DB_NAME")
    port = config.get("DB_PORT")
    host = config.get("DB_HOST")

    return create_engine(f"postgresql+psycopg://{username}:{password}@{host}:{port}/{name}", echo=True)


def create_tables(engine):
    metadata.drop_all(engine, checkfirst=True)
    metadata.create_all(engine, checkfirst=True)


def create_tables_orm(engine):
    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine, checkfirst=True)

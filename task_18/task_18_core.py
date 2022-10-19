from sqlalchemy import Table, Column, Integer, select, func, Text, DateTime, and_, distinct

from db import db_connect, create_tables, metadata

engine, connection = db_connect("postgres", "123456", "etoro")

tvprogram = Table(
    "tvprogram",
    metadata,
    Column("program_date", DateTime, nullable=False, primary_key=True),
    Column("content_id", Integer, nullable=False, primary_key=True),
    Column("channel", Text, nullable=False),
)

content = Table(
    "content",
    metadata,
    Column("content_id", Integer, primary_key=True),
    Column("title", Text, nullable=False),
    Column("kids_content", Text, nullable=False),
    Column("content_type", Text, nullable=False),
)

create_tables(engine)

new_tvprogram = [
    {"program_date": '2020-06-10 08:00', "content_id": 1, "channel": 'LC-Channel'},
    {"program_date": '2020-05-11 12:00', "content_id": 2, "channel": 'LC-Channel'},
    {"program_date": '2020-05-12 12:00', "content_id": 3, "channel": 'LC-Channel'},
    {"program_date": '2020-05-13 14:00', "content_id": 4, "channel": 'Disney Ch'},
    {"program_date": '2020-06-18 14:00', "content_id": 4, "channel": 'Disney Ch'},
    {"program_date": '2020-07-15 16:00', "content_id": 5, "channel": 'Disney Ch'},
]

new_content = [
    {"title": "Lost in space", "kids_content": "N", "content_type": "Movies"},
    {"title": "Alg. for Kids", "kids_content": "Y", "content_type": "Series"},
    {"title": "Database Sols", "kids_content": "N", "content_type": "Series"},
    {"title": "Aladdin", "kids_content": "Y", "content_type": "Movies"},
    {"title": "Cinderella", "kids_content": "Y", "content_type": "Movies"},
]

connection.execute(tvprogram.insert(), new_tvprogram)
connection.execute(content.insert(), new_content)

query = select(distinct(content.c.title)).\
    select_from(tvprogram.outerjoin(content, tvprogram.c.content_id == content.c.content_id)).\
    where(and_(func.to_char(tvprogram.c.program_date, 'yyyy-mm') == '2020-06',
               content.c.kids_content == 'Y', content.c.content_type == 'Movies'))


result = connection.execute(query)

for row in result:
    print(row)

connection.close()

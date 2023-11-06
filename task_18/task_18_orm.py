from sqlalchemy import Column, Integer, DateTime, Text, distinct, and_, func
from sqlalchemy.orm import aliased, Session

from db import Base


def task_18_orm(engine, create_tables):
    class TvProgram(Base):
        __tablename__ = "tvprogram"

        program_date = Column(DateTime, nullable=False, primary_key=True)
        content_id = Column(Integer, nullable=False, primary_key=True)
        channel = Column(Text, nullable=False)

    class Content(Base):
        __tablename__ = "content"

        content_id = Column(Integer, primary_key=True)
        title = Column(Text, nullable=False)
        kids_content = Column(Text, nullable=False)
        content_type = Column(Text, nullable=False)

    new_tvprogram = [
        TvProgram(program_date="2020-06-10 08:00", content_id=1, channel="LC-Channel"),
        TvProgram(program_date="2020-05-11 12:00", content_id=2, channel="LC-Channel"),
        TvProgram(program_date="2020-05-12 12:00", content_id=3, channel="LC-Channel"),
        TvProgram(program_date="2020-05-13 14:00", content_id=4, channel="Disney ChChannel"),
        TvProgram(program_date="2020-06-18 14:00", content_id=4, channel="Disney Ch"),
        TvProgram(program_date="2020-07-15 16:00", content_id=5, channel="Disney Ch"),
    ]

    new_content = [
        Content(title="Lost in space", kids_content="N", content_type="Movies"),
        Content(title="Alg. for Kids", kids_content="Y", content_type="Series"),
        Content(title="Database Sols", kids_content="N", content_type="Series"),
        Content(title="Aladdin", kids_content="Y", content_type="Movies"),
        Content(title="Cinderella", kids_content="Y", content_type="Movies"),
    ]

    Content.__table__.drop(engine, checkfirst=True)
    TvProgram.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_tvprogram)
        session.add_all(new_content)
        session.commit()

        t = aliased(TvProgram, name="t")
        c = aliased(Content, name="c")

        result = (
            session.query(distinct(c.title))
            .select_from(t)
            .outerjoin(c, t.content_id == c.content_id)
            .where(and_(
                func.to_char(t.program_date, "yyyy-mm") == "2020-06",
                c.kids_content == "Y", c.content_type == "Movies"
            )
            )
        )

        print(result.all())

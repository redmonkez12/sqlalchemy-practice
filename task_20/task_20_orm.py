from sqlalchemy import Column, Integer, Text, ForeignKey, func
from sqlalchemy.orm import Session

from db import Base


def task_20_orm(engine, create_tables):
    class Employee(Base):
        __tablename__ = "employees"

        employee_id = Column(Integer, primary_key=True)
        name = Column(Text, nullable=False)
        experience_years = Column(Integer, nullable=False)

    class Project(Base):
        __tablename__ = "projects"

        project_id = Column(Integer, primary_key=True)
        employee_id = Column(Integer, ForeignKey(Employee.employee_id, ondelete="CASCADE", onupdate="CASCADE"),
                             primary_key=True)

    new_employees = [
        Employee(name="Khaled", experience_years=3),
        Employee(name="Ali", experience_years=2),
        Employee(name="John", experience_years=1),
        Employee(name="Doe", experience_years=2),
    ]

    new_projects = [
        Project(project_id=1, employee_id=1),
        Project(project_id=1, employee_id=2),
        Project(project_id=1, employee_id=3),
        Project(project_id=2, employee_id=1),
        Project(project_id=2, employee_id=4),
    ]

    Project.__table__.drop(engine, checkfirst=True)
    Employee.__table__.drop(engine, checkfirst=True)
    create_tables()

    with Session(engine) as session:
        session.add_all(new_employees)
        session.add_all(new_projects)
        session.commit()

        result = (
            session.query(
                Project.project_id,
                func.round(func.avg(Employee.experience_years), 2).label("average_years"),
            ).outerjoin(Employee, Project.employee_id == Employee.employee_id)
            .group_by(Project.project_id)
        )

        print(result.all())

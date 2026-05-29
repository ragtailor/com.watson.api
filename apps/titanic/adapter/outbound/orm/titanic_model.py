from sqlalchemy import Column, Integer, String

from core.database import Base


class TitanicRecord(Base):
    __tablename__ = "titanic_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    passenger = Column(String, nullable=True)
    survived = Column(String, nullable=True)
    pclass = Column(String, nullable=True)
    name = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    age = Column(String, nullable=True)
    sibsp = Column(String, nullable=True)
    parch = Column(String, nullable=True)
    ticket = Column(String, nullable=True)
    fare = Column(String, nullable=True)
    cabin = Column(String, nullable=True)
    embarked = Column(String, nullable=True)

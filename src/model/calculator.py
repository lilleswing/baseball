from sqlalchemy import Column, Integer, String
from model import Base

__author__ = 'karl'


class Calculator(Base):
    __tablename__ = 'calculator'

    id = Column(Integer, primary_key=True)
    algorithm_name = Column(String(128))
    filter_name = Column(String(128))

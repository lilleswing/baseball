__author__ = 'leswing'
import json
from sqlalchemy import Column, Integer, TIMESTAMP
from model import Base

__author__ = 'leswing'


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    num = Column(Integer)
    indexer = Column(Integer)

    def to_json(self):
        d = {
            "id": self.id,
        }
        return json.dumps(d)
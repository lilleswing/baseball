import json
from sqlalchemy import Column, Integer, String
from model import Base

__author__ = 'leswing'



class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    batter = Column(Integer)
    pitcher = Column(Integer)
    event = Column(String(128))
    description = Column(String(1024))

    def to_json(self):
        d = {
            "id":self.id,
            "batter": self.batter,
            "pitcher": self.pitcher,
            "event": self.event,
            "description": self.description
        }
        return json.dumps(d)

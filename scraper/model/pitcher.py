import json
from model import Base
from sqlalchemy import Column, Integer, String

__author__ = 'leswing'


class Pitcher(Base):
    __tablename__ = 'pitcher'

    id = Column(Integer, primary_key=True)
    mlb_id = Column(Integer)
    name = Column(String(128))

    def __hash__(self):
        return hash(self.mlb_id)

    def __eq__(self, other):
        return self.mlb_id == other.mlb_id

    def to_json(self):
        d = {
            "id": self.id,
            "mlb_id": self.mlb_id,
            "name": self.name
        }
        return json.dumps(d)
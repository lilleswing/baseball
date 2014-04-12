import json
from model import Base
from sqlalchemy import Column, Integer, String

__author__ = 'leswing'

class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    mlb_id = Column(Integer)
    code = Column(String(128))
    name = Column(String(128))

    def to_json(self):
        d = {
            "id": self.id,
            "mlb_id": self.mlb_id,
            "code": self.code,
            "name": self.name
        }
        return json.dumps(d)

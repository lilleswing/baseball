__author__ = 'leswing'
import json
from sqlalchemy import Column, Integer
from model import Base

__author__ = 'leswing'


class Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    game_num = Column(Integer)

    def __init__(self, year, month, day, game_num):
        self.year = year
        self.month = month
        self.day = day
        self.game_num = game_num

    def __hash__(self):
        return hash((self.year, self.month, self.day, self.game_num))

    def __eq__(self, other):
        return (self.year, self.month, self.day, self.game_num) ==\
               (other.year, other.month, other.day, other.game_num)

    def to_json(self):
        d = {
            "id": self.id,
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "game_num": self.game_num
        }
        return json.dumps(d)
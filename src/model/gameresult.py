from sqlalchemy import Column, Integer, String, Float
from model import Base

__author__ = 'karl'


class GameResult(Base):
    __tablename__ = "game_result"

    id = Column(Integer, primary_key=True)
    calculator = Column(Integer)
    mlb_id = Column(Integer)
    player_type = Column(String(128))
    game = Column(Integer)
    actions = Column(Integer)
    score = Column(Float)



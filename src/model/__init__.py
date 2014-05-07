from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import settings
__author__ = 'leswing'


Base = declarative_base()
engine = create_engine(settings.database_url, echo=settings.database_echo)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def init():
    from model.event import Event
    from model.batter import Batter
    from model.pitcher import Pitcher
    from model.team import Team
    from model.game import Game
    from model.calculator import Calculator
    from model.gameresult import GameResult
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init()

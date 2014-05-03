from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
__author__ = 'leswing'


Base = declarative_base()
engine = create_engine('postgresql://postgres:NaClH2O@localhost:3247/baseball', echo=True)
#engine = create_engine('sqlite:///foo.db', echo=False)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def init():
    from model.event import Event
    from model.batter import Batter
    from model.pitcher import Pitcher
    from model.team import Team
    from model.game import Game
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init()
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
__author__ = 'leswing'


Base = declarative_base()
engine = create_engine('postgresql://postgres:NaClH2O@localhost/baseball', echo=True)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def init():
    from model.event import Event
    from model.batter import Batter
    from model.pitcher import Pitcher
    from model.team import Team
    Base.metadata.create_all(engine)


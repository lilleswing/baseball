import datetime
import json

import os
from sqlalchemy import Column, Integer, String
from sqlalchemy import Float
from sqlalchemy import TIMESTAMP
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import baseball.constants as constants
import baseball.settings as settings

__author__ = 'leswing'

Base = declarative_base()
engine = create_engine(settings.database_url, echo=settings.database_echo)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class Calculator(Base):
  __tablename__ = 'calculator'

  id = Column(Integer, primary_key=True)
  algorithm_name = Column(String(128))
  filter_name = Column(String(128))


class Batter(Base):
  __tablename__ = 'batter'

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


class Event(Base):
  __tablename__ = 'event'

  id = Column(Integer, primary_key=True)
  batter = Column(Integer)
  pitcher = Column(Integer)
  event = Column(String(128))
  description = Column(String(1024))
  at_bat = Column(Integer)
  game_id = Column(Integer)

  def to_json(self):
    d = {
      "id": self.id,
      "batter": self.batter,
      "pitcher": self.pitcher,
      "event": self.event,
      "description": self.description,
      "game_id": self.game_id
    }
    return json.dumps(d)

  def __str__(self):
    d = {
      "id": self.id,
      "batter": self.batter,
      "pitcher": self.pitcher,
      "event": self.event,
      "description": self.description,
      "game_id": self.game_id
    }
    return json.dumps(d)

  def __repr__(self):
    d = {
      "id": self.id,
      "batter": self.batter,
      "pitcher": self.pitcher,
      "event": self.event,
      "description": self.description,
      "game_id": self.game_id
    }
    return json.dumps(d)


class BatterPitcherMatrix:
  BATTER_ORIENTATION = "batter"
  PITCHER_ORIENTATION = "pitcher"

  def __init__(self, matrix, batters, pitchers, orientation, algorithm=None, matrix_filter=None):
    """
    NOTE(LESWING) eventually put in algorithm and filters here
    """
    self.orientation = orientation
    self.algorithm = algorithm
    self.matrix_filter = matrix_filter
    self.matrix = matrix
    self.batters = batters
    self.pitchers = pitchers
    self._create_lookup_tables()

  def get_cell(self, batter_mlbid, pitcher_mlbid):
    """
    Gets a cell in the matrix given the mlbid of the batter
    and pitcher
    """
    bat_index = self.batter_lookup[batter_mlbid]
    pit_index = self.pitcher_lookup[pitcher_mlbid]
    if self.orientation == constants.BATTER:
      return self.matrix[bat_index][pit_index]
    return self.matrix[pit_index][bat_index]

  def _create_lookup_tables(self):
    self.batter_lookup = self._create_lookup_table(self.batters)
    self.pitcher_lookup = self._create_lookup_table(self.pitchers)

  def _create_lookup_table(self, players):
    lookup = dict()
    for i in range(len(players)):
      player = players[i]
      lookup[player.mlb_id] = i
    return lookup


class Game(Base):
  __tablename__ = 'game'

  id = Column(Integer, primary_key=True)
  year = Column(Integer)
  month = Column(Integer)
  day = Column(Integer)
  game_num = Column(Integer)
  timestamp = Column(TIMESTAMP)

  def __init__(self, year, month, day, game_num):
    self.year = year
    self.month = month
    self.day = day
    self.game_num = game_num
    self.timestamp = datetime.datetime(year=year, month=month, day=day)

  def __hash__(self):
    return hash((self.year, self.month, self.day, self.game_num))

  def __eq__(self, other):
    return (self.year, self.month, self.day, self.game_num) == \
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

  def __repr__(self):
    return self.to_json()

  def __str__(self):
    return self.to_json()


class DbCollection():
  def __init__(self):
    self.batters = set()
    self.events = set()
    self.games = set()
    self.pitchers = set()
    self.teams = set()

  def join(self, dbcollection):
    self.batters.update(dbcollection.batters)
    self.games.update(dbcollection.games)
    self.pitchers.update(dbcollection.pitchers)
    self.teams.update(dbcollection.teams)
    self.events.update(dbcollection.events)

  def add_team(self, team):
    self.teams.add(team)

  def add_batter(self, batter):
    self.batters.add(batter)

  def add_pitcher(self, pitcher):
    self.pitchers.add(pitcher)

  def add_event(self, event):
    self.events.add(event)

  def commit(self):
    self.commit_collection(self.batters, Batter)
    self.commit_collection(self.pitchers, Pitcher)
    self.commit_collection(self.teams, Team)
    session.add_all(self.events)
    session.add_all(self.games)
    session.commit()

  def commit_collection(self, collection, claz):
    db_bat = session.query(claz).all()
    ids = set([x.mlb_id for x in db_bat])
    filtered_collection = filter(lambda x: x.mlb_id not in ids, collection)
    session.add_all(filtered_collection)
    session.commit()


class GameResult(Base):
  __tablename__ = "game_result"

  id = Column(Integer, primary_key=True)
  calculator = Column(Integer)
  mlb_id = Column(Integer)
  player_type = Column(String(128))
  game = Column(Integer)
  actions = Column(Integer)
  score = Column(Float)


def init():
  if os.path.exists(settings.database_filename):
    print("Not making database as already exists")
    return
  Base.metadata.drop_all(engine)
  Base.metadata.create_all(engine)
  print("Created Tables")


if __name__ == "__main__":
  init()
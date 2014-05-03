from model.batter import Batter
from model.pitcher import Pitcher
from model.team import Team

__author__ = 'karl'

from model import session


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




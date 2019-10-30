import datetime
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

import os

import constants
import traceback

from baseball.model import DbCollection
from baseball.model import Event
from baseball.model import Game, Team, Batter, Pitcher
from baseball.model import session

__author__ = 'leswing'

BOX_SCORE = "box_score"
EVENTS = "events"

HOME_TEAM = "home"
AWAY_TEAM = "away"


class EventsParser(object):
    def __init__(self, game_id):
        self.game_id = game_id
        self.collection = DbCollection()

    def save_half_inning(self, inning):
        try:
            at_bats = inning.findall('atbat')
            for at_bat in at_bats:
                attrib = at_bat.attrib
                event = Event()
                event.pitcher = int(attrib['pitcher'])
                event.batter = int(attrib['batter'])
                event.description = attrib['des']
                event.event = attrib['event']
                event.game_id = self.game_id
                self.collection.add_event(event)
        except Exception as e:
            traceback.print_exc()

    def parse(self, data):
        root = ET.fromstring(data)
        innings = root.findall('inning')
        for inning in innings:
            self.save_half_inning(inning.find('top'))
            self.save_half_inning(inning.find('bottom'))
        return self.collection


class BoxscoreParser(object):
    def __init__(self, game_num):
        self.game_num = game_num
        self.collection = DbCollection()

    def get_team(self, team_type, attrib):
        try:
            team = Team()
            team.code = attrib['%s_team_code' % team_type]
            team.name = attrib['%s_fname' % team_type]
            team.mlb_id = int(attrib['%s_id' % team_type])
            return team
        except:
            return None

    def save_team_names(self, root):
        home_team = self.get_team(HOME_TEAM, root.attrib)
        if home_team is not None:
            self.collection.add_team(home_team)
        away_team = self.get_team(AWAY_TEAM, root.attrib)
        if away_team is not None:
            self.collection.add_team(away_team)

    def save_batters(self, root):
        batting_sections = root.findall('batting')
        for batting_section in batting_sections:
            batters = batting_section.findall('batter')
            for batter_xml in batters:
                try:
                    attrib = batter_xml.attrib
                    batter = Batter()
                    if 'name_display_first_last' in attrib:
                        batter.name = attrib['name_display_first_last']
                    elif 'name' in attrib:
                        batter.name = attrib['name']
                    batter.mlb_id = int(attrib['id'])
                    self.collection.add_batter(batter)
                except:
                    print("error saving batter")

    def save_pitchers(self, root):
        pitching_sections = root.findall('pitching')
        for pitching_section in pitching_sections:
            pitchers = pitching_section.findall('pitcher')
            for pitcher_xml in pitchers:
                try:
                    attrib = pitcher_xml.attrib
                    pitcher = Pitcher()
                    if 'name_display_first_last' in attrib:
                        pitcher.name = attrib['name_display_first_last']
                    elif 'name' in attrib:
                        pitcher.name = attrib['name']
                    pitcher.mlb_id = int(attrib['id'])
                    self.collection.add_pitcher(pitcher)
                except:
                    print("error saving pitcher")

    def parse(self, data):
        root = ET.fromstring(data)
        self.save_team_names(root)
        self.save_batters(root)
        self.save_pitchers(root)
        return self.collection


def get_files(game):
    base = "%s/%4d.%02d.%02d.game_%d" % (constants.raw_xml_folder, game.year, game.month, game.day, game.game_num)
    boxscore = "%s%s" % (base, ".boxscore.xml")
    events = "%s%s" % (base, ".game_events.xml")
    return {
        BOX_SCORE: boxscore,
        EVENTS: events
    }


def has_game(game):
    files = get_files(game)
    for f in files.values():
        if not os.path.isfile(f):
            return False
    return True


def get_event_data(game):
    files = get_files(game)
    return open(files[EVENTS]).read()


def get_boxscore_data(game):
    files = get_files(game)
    return open(files[BOX_SCORE]).read()


def parse_boxscore(game, collection):
    try:
        box_parser = BoxscoreParser(game.id)
        box_collection = box_parser.parse(get_boxscore_data(game))
        collection.join(box_collection)
    except ParseError:
        print("Unable to parse boxscore for %s" % (game.to_json()))


def parse_events(game, collection):
    try:
        event_parser = EventsParser(game.id)
        event_collection = event_parser.parse(get_event_data(game))
        collection.join(event_collection)
    except ParseError:
        print("Unable to parse events for %s" % (game.to_json()))


if __name__ == '__main__':
    start_date = datetime.datetime(year=2008, month=1, day=1)
    game_set = set(session.query(Game).all())
    now = datetime.datetime.now()
    day = datetime.timedelta(days=1)
    collection = DbCollection()
    db_batch = 0
    while start_date < now:
        game = Game(start_date.year, start_date.month, start_date.day, 1)
        game.year = start_date.year
        game.month = start_date.month
        game.day = start_date.day
        while has_game(game):
            if game in game_set:
                game = Game(start_date.year, start_date.month, start_date.day, game.game_num + 1)
                continue
            session.add(game)
            session.commit()
            db_batch += 1
            parse_boxscore(game, collection)
            parse_events(game, collection)
            game = Game(start_date.year, start_date.month, start_date.day, game.game_num + 1)
            if db_batch % 1000 == 0:
                collection.commit()
                collection = DbCollection()

                start_date += day
        collection.commit()

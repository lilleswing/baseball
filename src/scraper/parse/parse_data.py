from xml.etree.ElementTree import ParseError
import datetime
import os
from model import session
from model.dbcollection import DbCollection
from model.game import Game
from scraper.parse.boxscore_parser import BoxscoreParser
from scraper.parse.events_parser import EventsParser
import settings

__author__ = 'leswing'

BOX_SCORE = "box_score"
EVENTS = "events"

global game_set
start_date = datetime.datetime(year=2008, month=1, day=1)


def get_files(game):
    base = "%s/%4d.%02d.%02d.game_%d" % (settings.raw_xml_folder, game.year, game.month, game.day, game.game_num)
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
        print "Unable to parse boxscore for %s" % (game.to_json())


def parse_events(game, collection):
    try:
        event_parser = EventsParser(game.id)
        event_collection = event_parser.parse(get_event_data(game))
        collection.join(event_collection)
    except ParseError:
        print "Unable to parse boxscore for %s" % (game.to_json())


if __name__ == '__main__':
    global game_set
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

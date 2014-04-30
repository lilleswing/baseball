from model import session
from model.batter import Batter
from model.event import Event
from model.parsedfile import ParsedFile
from model.pitcher import Pitcher
from model.team import Team
from os import listdir
from os.path import isfile, join
import re
import traceback
import xml.etree.ElementTree as ET

__author__ = 'leswing'

raw_xml_folder = 'rawxml'
pitchers_set = set()
batters_set = set()
file_set = set()

HOME_TEAM = "home"
AWAY_TEAM = "away"


def get_team(team_type, attrib):
    try:
        team = Team()
        team.code = attrib['%s_team_code' % team_type]
        team.name = attrib['%s_fname' % team_type]
        team.mlb_id = int(attrib['%s_id' % team_type])
        return team
    except:
        return None


def save_team_names(root):
    home_team = get_team(HOME_TEAM, root.attrib)
    if home_team is not None:
        team = session.query(Team).filter(Team.mlb_id == home_team.mlb_id).all()
        if len(team) < 1:
            session.add(home_team)
    away_team = get_team(AWAY_TEAM, root.attrib)
    if away_team is not None:
        team = session.query(Team).filter(Team.mlb_id == away_team.mlb_id).all()
        if len(team) < 1:
            session.add(away_team)

    session.commit()


def save_batters(root):
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
                batters_set.add(batter)
            except:
                print("error saving batter")


def save_pitchers(root):
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
                pitchers_set.add(pitcher)
            except:
                print("error saving pitcher")


def parse_box_scores():
    files = [f for f in listdir(raw_xml_folder) if isfile(join(raw_xml_folder, f))]
    boxscores = [f for f in files if re.match(".*boxscore.xml", f) and f not in file_set]
    boxscores = sorted(boxscores)
    for boxscore in boxscores:
        try:
            xml_data = open('%s/%s' % (raw_xml_folder, boxscore)).read()
            root = ET.fromstring(xml_data)
            save_team_names(root)
            save_batters(root)
            save_pitchers(root)
            indexed = ParsedFile(boxscore)
            session.add(indexed)
            session.commit()
        except:
            print("error with boxscore %s" % boxscore)
            traceback.print_exc()
            continue
    session.add_all(list(batters_set))
    session.add_all(list(pitchers_set))
    session.commit()


def save_half_inning(inning):
    at_bats = inning.findall('atbat')
    events = list()
    for at_bat in at_bats:
        attrib = at_bat.attrib
        event = Event()
        event.pitcher = int(attrib['pitcher'])
        event.batter = int(attrib['batter'])
        event.description = attrib['des']
        event.event = attrib['event']
        events.append(event)
    return events


def save_events(root):
    innings = root.findall('inning')
    events = list()
    for inning in innings:
        events.extend(save_half_inning(inning.find('top')))
        events.extend(save_half_inning(inning.find('bottom')))
    session.add_all(events)
    session.commit()


def parse_game_events():
    files = [f for f in listdir(raw_xml_folder) if isfile(join(raw_xml_folder, f))]
    events = [f for f in files if re.match(".*events.xml", f) and f not in file_set]
    events = sorted(events)
    for event in events:
        try:
            xml_data = open('%s/%s' % (raw_xml_folder, event)).read()
            root = ET.fromstring(xml_data)
            save_events(root)
            indexed = ParsedFile(event)
            session.add(indexed)
            session.commit()
        except:
            print("error with event %s" % event)
            traceback.print_exc()
            continue


if __name__ == '__main__':
    global file_set
    parsed = session.query(ParsedFile).all()
    file_set = set([x.filename for x in parsed])
    parse_box_scores()
    parse_game_events()

import xml.etree.ElementTree as ET
from model.batter import Batter
from model.dbcollection import DbCollection
from model.pitcher import Pitcher
from model.team import Team

__author__ = 'karl'

HOME_TEAM = "home"
AWAY_TEAM = "away"


class BoxscoreParser():
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

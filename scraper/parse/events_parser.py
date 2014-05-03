from model.dbcollection import DbCollection
import xml.etree.ElementTree as ET
from model.event import Event

__author__ = 'karl'


class EventsParser():

    def __init__(self, game_id):
        self.game_id = game_id
        self.collection = DbCollection()

    def save_half_inning(self, inning):
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

    def parse(self, data):
        root = ET.fromstring(data)
        innings = root.findall('inning')
        for inning in innings:
            self.save_half_inning(inning.find('top'))
            self.save_half_inning(inning.find('bottom'))
        return self.collection





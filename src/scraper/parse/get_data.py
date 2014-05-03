from datetime import timedelta, datetime
import re
import traceback

from sqlalchemy import desc

from model import session
from model.game import Game
import requests


__author__ = 'leswing'


base_url = "http://gd2.mlb.com/components/game/mlb"
rawxml_folder = 'rawxml'


def create_url(year, month, day):
    return "%s/year_%04d/month_%02d/day_%02d" % (base_url, year, month, day)


def download_xml(year, month, day):
    url = create_url(year, month, day)
    r = requests.get(url)
    links = get_links(url, year, month, day, r.text)
    for i in xrange(0, len(links)):
        link = links[i]
        save_to_file(link, "boxscore.xml", year, month, day, i)
        save_to_file(link, "game_events.xml", year, month, day, i)


def save_to_file(url, extension, year, month, day, game_num):
    try:
        full_url = "%s/%s" % (url, extension)
        r = requests.get(full_url)
        filename = "%s/%04d.%02d.%02d.game_%d.%s" % (rawxml_folder, year, month, day, game_num, extension)
        f = open(filename, 'w')
        f.write(r.text.encode('utf-8'))
        f.close()
    except:
        traceback.print_exc()
        print("unable to load %s, %s" % (url, extension))


def get_links(url, year, month, day, text):
    pattern = 'gid_%04d_%02d_%02d.*?"' % (year, month, day)
    rel_links = re.findall(pattern, text)
    rel_links = [x[0:-2] for x in rel_links]
    links = ["%s/%s" % (url, x) for x in rel_links]
    links = sorted(links)
    return links


def download_dates(start):
    now = datetime.datetime.now()
    day = timedelta(days=1)
    while start < now:
        download_xml(start.year, start.month, start.day)
        start += day


def full_download():
    first = datetime.datetime(year=2008, month=1, day=1)
    download_dates(first)


def incremental_download():
    last = session.query(Game).order_by(desc(Game.timestamp)).first()
    download_dates(last)

if __name__ == '__main__':
    incremental_download()


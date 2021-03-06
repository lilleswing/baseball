import constants
import os
import re
import requests
import traceback
from datetime import timedelta, datetime
from model import session
from model import Game
from sqlalchemy import desc

__author__ = 'leswing'


def create_url(year, month, day):
    return "%s/year_%04d/month_%02d/day_%02d" % (constants.base_scrape_url, year, month, day)


def download_xml(year, month, day):
    url = create_url(year, month, day)
    r = requests.get(url)
    links = get_links(url, year, month, day, r.text)
    for i in range(0, len(links)):
        link = links[i]
        save_to_file(link, "boxscore.xml", year, month, day, i)
        save_to_file(link, "game_events.xml", year, month, day, i)


def save_to_file(url, extension, year, month, day, game_num):
    try:
        full_url = "%s/%s" % (url, extension)
        print(full_url)
        filename = "%s/%04d.%02d.%02d.game_%d.%s" % (constants.raw_xml_folder, year, month, day, game_num, extension)
        if os.path.exists(filename):
            return

        r = requests.get(full_url)
        with open(filename, encoding='utf-8', mode='w+') as f:
            f.write(r.text)
    except:
        traceback.print_exc()
        print("unable to load %s, %s" % (url, extension))


def get_links(url, year, month, day, text):
    pattern = 'gid_%04d_%02d_%02d.*?"' % (year, month, day)
    rel_links = re.findall(pattern, text)
    rel_links = [x[0:-2] for x in rel_links]
    rel_links = list(filter(lambda x: x.find('<li>') == -1, rel_links))
    links = ["%s/%s" % (url, x) for x in rel_links]
    links = sorted(links)
    return links


def download_dates(start):
    day = timedelta(days=1)
    now = datetime.now() - day  # MLB.com puts empty files up before the games are actually played day of
    while start < now:
        download_xml(start.year, start.month, start.day)
        start += day


def full_download():
    first = datetime(year=2008, month=1, day=1)
    download_dates(first)


def incremental_download():
    last = session.query(Game).order_by(desc(Game.timestamp)).first()
    if last is None:
        full_download()
    else:
        download_dates(last.timestamp)


if __name__ == '__main__':
    incremental_download()

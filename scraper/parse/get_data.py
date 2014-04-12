__author__ = 'leswing'
import requests
import re
import traceback

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
        filename = "%s/%04d.%02d.%02d.game_%d.%s" %(rawxml_folder, year, month, day, game_num, extension)
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


if __name__=='__main__':
    years = ['2008','2009','2010','2011','2012','2013']
    for year in xrange(2008,2014):
        for month in xrange(1,13):
            for day in xrange(1,32):
                download_xml(year, month, day)





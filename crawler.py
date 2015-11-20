import json
import urllib2

__author__ = 'sebastian'


DATASET = 'http://data.opendatasoft.com/api/records/1.0/search?dataset=open-data-sources%40public&facet=country&facet=organisation&facet=name'

SOFTWARE = ['ckan', 'socrata', 'datapress', 'dataverse', 'dkan', 'junar', 'ogdi', 'opendatasoft',  'publishmydata']

class PortalsList:
    def __init__(self, rows=10):
        self.rows=rows

    def iter(self):
        start = 0
        while True:

            query = DATASET + '&rows=' + str(self.rows) + '&start=' + str(start)
            requ = urllib2.urlopen(query)
            data = json.loads(requ.read())
            portals = data['records']
            if len(portals) == 0:
                break

            for p in portals:
                yield p['fields']

            start += self.rows


def get_html(url):
    requ = urllib2.urlopen(url, timeout=5)
    return requ.read()


if __name__ == '__main__':
    portals_iter = PortalsList()

    tmp = []
    for p in portals_iter.iter():
        url = p['url']
        print '#####################################'
        print url
        try:
            html = get_html(url).lower()
            p['retrievable'] = True
            print 'RETRIEVABLE'

            for s in SOFTWARE:
                if s in html:
                    if 'software' in p:
                        p['software_alternative'] = p.get('software_alternative', []).append(s)
                        print 'SOFTWARE', s
                    else:
                        p['software'] = s
                        print 'SOFTWARE', s
        except Exception as e:
            print 'ERROR'
            print e
            p['retrievable'] = False

        tmp.append(p)

    with open('portals.json', 'w')as f:
        json.dump(tmp, f)


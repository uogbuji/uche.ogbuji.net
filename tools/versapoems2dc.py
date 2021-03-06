import sys
import datetime
import operator

from amara3 import iri
from versa import I, VERSA_BASEIRI, ORIGIN, RELATIONSHIP, TARGET, ATTRIBUTES
from versa.driver import memory
from versa.reader.md import from_markdown
from versa.util import simple_lookup

VTYPE = I(iri.absolutize('type', VERSA_BASEIRI))

def resources_by_type(m, rtype):
    return [ link[ORIGIN] for link in m.match(None, VTYPE, rtype) ]

def parse_date(d):
    '''
    Take a brute force approach to parsing ISO dates
    '''
    try:
        return datetime.datetime.strptime(d, '%Y-%m-%d')
    except ValueError:
        try:
            return datetime.datetime.strptime(d, '%Y-%m')
        except ValueError:
            return datetime.datetime.strptime(d, '%Y')

def run(infile):
    m = memory.connection()
    from_markdown(infile.read(), m)
    #from versa.util import jsondump
    #jsondump(m, open('/tmp/foo.json', 'w'))
    print('<descriptionSet>')
    for poem in resources_by_type(m, 'http://uche.ogbuji.net/poems/poem'):
        choice = '@choice' in list(map(operator.itemgetter(TARGET), m.match(poem, 'http://www.w3.org/2005/Atom/category')))
        if not choice: continue
        print('<description>')
        d = parse_date(simple_lookup(m, poem, 'http://www.w3.org/2005/Atom/updated'))
        source = next(m.match(poem, 'http://www.w3.org/2005/Atom/source'))
        source = source[ATTRIBUTES]['title']
        title = simple_lookup(m, poem, 'http://www.w3.org/2005/Atom/title')
        print('  <title>{0}</title>\n  <date>{1}</date>\n  <publisher>{2}</publisher>'.format(title, d.strftime('%B, %Y'), source))
        hlink = list(map(operator.itemgetter(TARGET), m.match(poem, 'http://www.w3.org/2005/Atom/link')))
        if hlink:
            hlink = hlink[0]
            print('  <link href="{0}"/>'.format(hlink))
        print('</description>')
    print('</descriptionSet>')

run(open(sys.argv[1]))

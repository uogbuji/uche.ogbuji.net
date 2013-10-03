import os, sys, datetime
from dateutil import parser as dateparser #pip install python-dateutil

from copy import deepcopy
from amara import parse
from amara.bindery import html
from amara.tools import atomtools
from amara.writers.struct import structwriter, E, NS, ROOT, RAW, E_CURSOR
from amara.namespaces import ATOM_NAMESPACE, XML_NAMESPACE, XHTML_NAMESPACE
from amara.lib import U
from amara.lib.util import strip_namespaces #,unwrap

def pretty_date(dt):
    #https://pypi.python.org/pypi/py-pretty
    #pip install py-pretty
    import pretty
    prettied = pretty.date(dt)
    return prettied


def dumb_copy(node):
    #Because copy.deepcopy doesn't always work
    serial = node.xml_encode()
    new_node = parse(serial)
    return new_node.xml_first_child


def xml_encode_fragment(nodes, encoding='utf-8'):
    #FIXME: support same args as xml_encode method
    '''
    nodes = e.g. foo.xml_children
    '''
    chunks = []
    for child in nodes:
        chunks.append(child.xml_encode(encoding=encoding))
    return ''.join(chunks)


def main_link(e):
    for link in e.link:
        if not link.rel:
            return U(link.href)


def other_links(e):
    links = list(e.link)
    for link in links:
        if not link.rel:
            links.remove(link)
    if not links:
        return ()
    return (
             E(u'div', {u'class': u'seealso-wrapper'},
             u'See also:',
             E(u'ul', {u'class': u'seealso'},
               ( E(u'li', {u'class': U(link.rel)}, U(link.href) ) for link in links ),
             ))
           )


class event_handler(object):
    def __init__(self, fullfeed, choicefeed):
        self.fullfeed = fullfeed
        self.choicefeed = choicefeed

    def execute(self, e):
        summary = dumb_copy(e.summary.div)
        strip_namespaces(summary) #, strip_decls=True
        summary = xml_encode_fragment(summary.xml_children)
        summary = summary.replace(' xmlns:dc="http://purl.org/dc/elements/1.1/"', '')
        summary = summary.replace(' xmlns=""', '')

        #Ignore this one
        elem = E(u'section',
            E(u'h2',
                E(u'a', {u'href': main_link(e)}, U(e.title))
            ),
            ( E(u'h3', U(subtitle)) for subtitle in (e.subtitle or []) if U(subtitle).strip() ),
            (E(u'div', {u'class': u'author'},
                E(u'div', {u'class': u'author-name'}, U(a.name or '')),
                E(u'div', {u'class': u'author-email'}, U(a.email or '')),
                E(u'div', {u'class': u'author-uri'}, U(a.uri or ''))
            ) for a in e.author ),
            E(u'div', {u'class': u'updated'}, U(e.updated)),
            E(u'div', {u'class': u'summary'}, RAW(summary)),
            E(u'ul', {u'class': u'keywords'},
                ( E(u'li', U(c.term) ) for c in (e.category or []) if U(c.term).strip() and U(c.term).strip() != U'@choice' ),
            ),
            other_links(e),
        )

        elem = E(u'section',
            E(u'a', {u'href': main_link(e)},
                E(u'h2', U(e.title)),
                [ E(u'h3', U(subtitle)) for subtitle in (e.subtitle or []) if U(subtitle).strip() ],
                #E(u'div', {u'class': u'updated'}, pretty_date(dateparser.parse(U(e.updated)))),
                #http://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
                E(u'p', {u'class': u'source'}, E(u'cite', U(e.source.title) + u','), u' ' + dateparser.parse(U(e.updated)).strftime('%B, %Y')),
                RAW(summary),
            )
        )

        self.fullfeed.send(elem)
        if e.category and U'@choice' in [ U(c.term).strip() for c in e.category ]:
            self.choicefeed.send(elem)


def run(input=None, outfullhtml=None, outfulljson=None, outchoicehtml=None):
    pubfeed = atomtools.feed('http://uche.ogbuji.net/publications', input)

    output = structwriter(stream=outfullhtml, indent=u"yes")
    fullfeed = output.cofeed(ROOT(E_CURSOR(u'div', {u'class': u'articles'})))

    output = structwriter(stream=outchoicehtml, indent=u"yes")
    choicefeed = output.cofeed(ROOT(E_CURSOR(u'div', {u'class': u'articles'})))

    h = event_handler(fullfeed, choicefeed)

    for e in list(pubfeed.feed.entry):
        h.execute(e)

    fullfeed.close()
    choicefeed.close()


#U(c.term).strip() != U'@choice'

# Handle the command-line arguments

from akara.thirdparty import argparse #Sorry PEP 8 ;)

#import signal
#import shutil

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(prog="bootstrap", add_help=False)
    parser = argparse.ArgumentParser()
    #parser.add_argument('-o', '--output')
    parser.add_argument('input', type=argparse.FileType('r'), metavar='INPUT',
                        help='Input atom file')
    parser.add_argument('-o', '--out',
        help='file path and name stem stem of the 3 files to be written')
    #
    args = parser.parse_args()
    outfullhtml = open(args.out + '.full.html', 'w')
    outfulljson = open(args.out + '.full.json', 'w')
    outchoicehtml = open(args.out + '.choice.html', 'w')

    run(input=args.input, outfullhtml=outfullhtml, outfulljson=outfulljson, outchoicehtml=outchoicehtml)
    args.input.close()


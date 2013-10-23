import sys
from amara.tools import atomtools
from amara.lib import U
from amara.writers.struct import *

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
	           ( E(u'li', {u'class': U(link.rel)}, U(link.href) ) for link in links if None not in (link.rel, link.href) ),
	         ))
	       )

pubfeed = atomtools.feed('http://uche.ogbuji.net/publications', sys.argv[1])

w = structwriter(indent=u"yes").feed(
ROOT(
  E(u'div', {u'class': u'articles'},
    (
      E(u'article',
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
        E(u'div', {u'class': u'summary'}, U(e.summary)),
        E(u'ul', {u'class': u'keywords'},
          ( E(u'li', U(c.term) ) for c in e.category if U(c.term).strip() ),
        ),
        other_links(e),
    ) for e in pubfeed.feed.entry )
  )
))





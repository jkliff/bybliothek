import urllib
import lxml.html
import lxml.html.clean
import sys
import re

def parse_book_info (t):
    condensed = ''.join (map (lambda x: x.strip (), t.split ("\n")))
    m = re.search ('<.*><b>(.*)</b><br><span class=\"small\">.*<a href=\"[a-zA-Z/_\.]+">([\.\w\s,]*)</a>.*<br>Publisher.*<a href=\".*\">(.*)</a>.*</span></div>', condensed)
    title = m.group (1)
    author = m.group (2)
    publisher = m.group (3)
    return {'title': title, 
            'author': author, 
            'publisher': publisher
    }

def lookup_isbn (isbn):

    root = lxml.html.parse ('http://isbndb.com/search-all.html?kw=%s' % isbn).getroot ()

    info = root.cssselect ('div.bookInfo')
    if info is None or len (info) == 0:
        return None
    else:
        return parse_book_info (lxml.html.tostring (info[0]))

if __name__ == '__main__':
    isbn = sys.argv[1]
    print lookup_isbn (isbn)

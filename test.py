import unittest

import isbn_finder

test_data = ["""<div class="bookInfo"><b>Gerechtigkeitstheorien zur EinfA&#195;&#130;&#194;&#188;hrung</b><br><span class="small"><a href="/d/person/bernd_ladwig.html">Bernd Ladwig</a>,  <br>Publisher: <a href="/d/publisher/junius_verlag_gmbh.html">Junius Verlag Gmbh</a><br>ISBN: 3885066939&#160;&#160;Edition: Perfect Paperback; 2011-07-01</span></div>""",
    """<div class="bookInfo"><b>Set theory and logic</b><br><span class="small">by  <a href="/d/person/stoll_robert_roth.html">Robert R. Stoll</a><br>Publisher: New York : <a href="/d/publisher/dover_publications.html">Dover Publications</a>, 1979, c1963.<br>ISBN: 0486638294&#160;&#160;</span></div>""",
    """<div class="bookInfo"><b>Refactoring</b><br><span class="small">Refactoring: improving the design of existing code<br><a href="/d/person/fowler_martin.html">Martin Fowler</a><br>Publisher: Reading, MA : <a href="/d/publisher/addison_wesley.html">Addison-Wesley</a></span></div>""",
    """<div class="bookInfo"><b>Refactoring</b><br><span class="small">Refactoring: improving the design of existing code<br><a href="/d/person/fowler_martin.html">Martin Fowler</a>; with contributions by  <a href="/d/person/beck_kent.html">Kent Beck</a>... [et al.] <br>Publisher: Reading, MA : <a href="/d/publisher/addison_wesley.html">Addison-Wesley</a>, 1999.<br>ISBN: 0201485672&#160;&#160;DDC: 5.14&#160;&#160;LCC: QA76.76&#160;&#160;</span></div>"""]

class BasicTest(unittest.TestCase):
    def test_parse_book_info (self):
        global test_data
        for t in test_data:
            r = isbn_finder.parse_book_info (t)
            print r




if __name__ == '__main__':
    unittest.main()

import cherrypy
import json
import os
import pprint
import datetime
import psycopg2

CWD = os.path.dirname(os.path.abspath(__file__))

DB_CONF = 'dbname = books user=john host=localhost'

STATIC_CONF = {
    '/': {
        'tools.staticdir.root': CWD,
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'www',
        'tools.staticdir.index': 'index.html'
    }
}

BOOK_CONF = {'/': {
        'request.dispatch': cherrypy.dispatch.MethodDispatcher ()
    }
}

class BookRepresentation:
    def __init__ (self):
        self.isbn = None
        self.author = None
        self.title = None
        self.created = None
        self.updated = None
        
    def as_dict (self):
        return {'id': self.__id, 'data': self.__data, 'created': self.__created, 'updated': self.__updated}
    def tojson (self):
        return json.dumps (self.as_dict())
    def tostr (self):
        return 'foo %s: %s' % (self.__id, self.__data)
    def set_data (self, d):
        self.__data = d
        self.__updated = str (datetime.datetime.now())

#def init_repository (size=10):
#    _respository = {}
#    for i in range (size):
#        f = BookRepresentation(i)
#        f.set_data ('x' * i)
#        _respository [str(i)] = f
#
#    return _respository

class Root: 
    pass

def load_book (id):
    sql = 'select b_id, isbn, author, title from books.book where b_id = ?'
    with () as conn: 
        c = conn.cursor ()
        r = c.execute (sql)
        return r

def load_all_books ():
    sql = 'select b_id, isbn, author, title from books.book order by b_id'
    global DB_CONF
    conn = psycopg2.connect (DB_CONF)
    c = conn.cursor ()
    c.execute (sql)
    r = c.fetchall()
    print r
    c.close()
    conn.close()
    return map (lambda x: {'id': x[0], 'isbn': x[1], 'author': x[2], 'title': x[3]}, r)

def update_book (id, data):
    sql = 'update books.book set isbn = ?, author = ?, title = ? where b_id = ?'

def remove_book (id):
    sql = 'delete from books.book where b_id = ?'

class BooksREST:
    exposed = True
    def __init__ (self):
        #self._respository = init_repository ()
        pass
    def GET (self, id=None):
        print id
        print 'get', id
        if id is not None:
            return json.dump (load_book (id))
            
        else:
            return json.dumps (load_all_books())
    def POST (self, id, data):
        update_book (id, json.reads (data))
    def PUT (self, data):
        
        r = insert_book (json.reads (data)['isbn'])
        return json.dumps (r)
    def DELETE (self, id):
        remove_book (id)

def parse_opts ():
    from argparse import ArgumentParser
    parser = ArgumentParser (description = 'pybliothek server')
    parser.add_argument('-H', '--host', default = '0.0.0.0')
    parser.add_argument('-P', '--port', default = 9999, type=int)
    
    args = parser.parse_args ()
    return (args.host, args.port)

###############################################################################

def main ():

    (host, port) = parse_opts ()

    cherrypy.config.update({
        'server.socket_host': host,
        'server.socket_port': port,
    })

    cherrypy.tree.mount (Root(), '/', config=STATIC_CONF)
    cherrypy.tree.mount (BooksREST(), '/book', config=BOOK_CONF)

    cherrypy.engine.start()
    cherrypy.engine.block()
###############################################################################
if __name__ == '__main__':
    main ()


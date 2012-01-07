
import json
import web
import psycopg2

urls = (
    '/',    'root',
    '/jquery.js', 'jquery', 
    '/jquery.dataTables.min.js', 'jquery_dataTables',
    '/list', 'list',
    '/add', 'add')

files = {
    'index.html': None,
    'jquery.js': None,
    'jquery.dataTables.min.js': None
}

for i in files.keys():
    with (open ('www/'+ i)) as f:
        files[i] = f.read()
        print i, len (files[i])

class list:
    def GET (self):
        conn = psycopg2.connect ('dbname = books')
        cur = conn.cursor ()
        cur.execute ('select author, title, isbn from books.book')
        r = cur.fetchall ()
        conn.commit ()
        cur.close()
        conn.close()

        return json.dumps (r)

class add:
    def POST(self, name):
        pass
class jquery_dataTables:
    def GET (self):
        global files
        return files ['jquery.dataTables.min.js']
class jquery:
    def GET (self):
        global files
        return files ['jquery.js']

class root:
    def GET (self):
        global files
        return files ['index.html']

app = web.application (urls, globals())

if __name__ == '__main__':
    app.run()


from flask import Flask, g
import random
import sqlite3

class LazyRoute(object):
	def __init__(self, app, path):
		self._app = app
		self._path = path

	def get(self, query_template, path=None):
		method_path = self._path + "/" + path if path is not None else self._path

		def view(**kwargs):
			query = query_template.format(**kwargs)
			print query
			cur = self._app.db.execute(str(query))
			rv = cur.fetchall()
			cur.close()
			return "Hi! %s" % rv
		view.__name__ = 'view_%d' % random.randint(1,999)
		self._app.route(method_path, methods=["GET"])(view)


class LazyRest(Flask):
	def __init__(self, db_path):
		super(LazyRest, self).__init__('hi')
		self._db_path = db_path

  	def _request_has_connection(self):
  		return hasattr(g, 'dbconn')

  	@property
  	def db(self):
  		if not self._request_has_connection():
  			g.dbconn = sqlite3.connect(self._db_path)
  		return g.dbconn

	def lazyroute(self, path):
		route = LazyRoute(self, path)
		return route

if __name__ == '__main__':
    app = LazyRest('database.db')
    app.debug = True
    index = app.lazyroute("/index")
    index.get("select * from blah")
    index.get('select * from blah where name=?', "<name>")
    app.run()
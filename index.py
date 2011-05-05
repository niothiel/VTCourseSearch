import web

urls = (
	'/', 'index',
	'/add', 'add',
	'/main.css', 'static'
)

app = web.application(urls, globals())
render = web.template.render('./templates/')
db = web.database(dbn='mysql', db='VTCS')

class index:
	def GET(self):
		courses = db.select('Courses')
		return render.index(courses)

class add:
	def POST(self):
		i = web.input()
		n = db.insert('Courses', email=i.email, crn=i.crn)
		raise web.seeother('/')

class static:
	def GET(self):
		fh = file('main.css', 'r')
		return fh.read();
		

if __name__ == "__main__":
	app.run()

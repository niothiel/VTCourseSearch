import web
from csadapter import *
from dbadapter import *

urls = (
	'/', 'index',
	'/login', 'login',
	'/logout', 'logout',
	'/register', 'register',
	'/about', 'about',
	'/add', 'add',
	'/status', 'status'
)

app = web.application(urls, globals())
render = web.template.render('./templates/')
#dbobj = web.database(dbn='mysql', db='VTCS')
db = DBAdapter( web.database(dbn='mysql', db='VTCS') )
cs = CSAdapter()

# Workaround with Debug mode because of reloader issues
if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore('sessions'), initializer = {'login': 0})
	web.config._session = session
else:
	session = web.config._session

class index:
	def GET(self):
		#courses = db.select('Courses')
		#body = render.index(courses);
		body = "An Intro and directions should go here."
		return render.skeleton(session, body)

class login:
	def GET(self):
		body = render.login()
		return render.skeleton(session, body)

	def POST(self):
		email = web.input().email
		passwd = web.input().passwd

		result = db.login(email, passwd)

		if result:
			session.login = 1
			session.email = email
			body = render.login_success()
		else:
			session.login = 0
			session.email = None
			body = render.login_failure()
		
		return render.skeleton(session, body)

class logout:
	def GET(self):
		session.kill();
		web.seeother('/')

class register:
	def GET(self):
		body = render.register();
		return render.skeleton(session, body);

class about:
	def GET(self):
		body = render.about();
		return render.skeleton(session, body)

class add:
	def GET(self):
		body = render.add(cs.getTerms())
		return render.skeleton(session, body)

	def POST(self):
		body = "Coming soon.<br>"

		for entry in web.input():
			body += entry + '='
			body += web.input()[entry]
			body += '<br>'
		
		return render.skeleton(session, body)

class status:
	def GET(self):
		body = "Coming soon."
		return render.skeleton(session, body)

if __name__ == "__main__":
	app.run()

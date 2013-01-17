import web
from csadapter import *
from dbadapter import *
from validator import *
from notifier import Notifier
from checker import check_availability

from pprint import pprint

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
# This one isn't completely compatible anymore
#db = ShelfDBAdapter()
db = MongoDBAdapter()
cs = CSAdapter()
valid = Validator()
notifier = Notifier()

# Workaround with Debug mode because of reloader issues
if web.config.get('_session') is None:
	session = web.session.Session(app, web.session.DiskStore('sessions'), initializer = {'login': False})
	web.config._session = session
else:
	session = web.config._session

class index:
	def GET(self):
		body = render.index()
		return render.skeleton(session, body)

class login:
	def GET(self):
		body = render.login()
		return render.skeleton(session, body)

	def POST(self):
		email = web.input().email
		passwd = web.input().passwd

		if db.is_login_valid(email, passwd):
			session.login = True
			session.email = email
			body = render.login_success()
		else:
			session.login = False
			session.email = None
			body = render.login_failure()
		
		return render.skeleton(session, body)

class logout:
	def GET(self):
		session.kill()
		web.seeother('/')

class register:
	def GET(self):
		body = render.register()
		return render.skeleton(session, body)

	def POST(self):
		email = web.input().email
		passwd = web.input().passwd
		phone = web.input().phone

		body = ''

		if not valid.email(email):
			body += 'The email you entered is invalid!'
		elif len(passwd) < 4:
			body += 'The password must be at least 4 characters long.'
		elif db.does_email_exist(email):
			body += 'That email is already in use!'
		else:
			db.add_user(email, passwd, phone)
			body += 'You have successfully registered! Please log in and add your courses.'

		return render.skeleton(session, body)

class about:
	def GET(self):
		body = render.about()
		return render.skeleton(session, body)

class add:
	def GET(self):
		body = render.add(cs.get_terms())
		return render.skeleton(session, body)

	def POST(self):
		data = web.input()

		term = None
		crns = []

		for entry in web.input():
			if entry == 'term':
				term = data[entry]
			elif len(data[entry]) != 0:
				crn = int(data[entry])
				crns.append(crn)

		email = session.email

		print term, crns, email
		for crn in crns:
			if not cs.crn_exists(term, crn):
				body = "That doesn't appear to be a valid course number.. You entered: " + str(crn)
				return render.skeleton(session, body)

			if not db.add_course(email, crn, term):
				body = "An error has occured while trying to add the course to the datebase (Duplicate course?)"
				return render.skeleton(session, body)

		web.seeother('/status')

class status:
	def GET(self):
		courses = db.get_courses(session.email)
		print 'Courses:', len(courses)
		pprint(courses)
		check_availability(cs, db, notifier, session.email)
		
		body = render.status(courses)
		return render.skeleton(session, body)

	def POST(self):
		for value in web.input().values():
			crn, term = value.split(',')
			crn = int(crn)
			term = int(term)

			print 'Deleting Course:', value, crn, term
			db.delete_course(session.email, crn, term)

		web.seeother('/status')

if __name__ == "__main__":
	app.run()

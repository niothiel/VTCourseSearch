from web.db import sqlquote

class DBAdapter:
	def __init__(self, db):
		self.db = db

	def login(self, email, passwd):
		myvars = {'email': email, 'passwd': passwd}
		ident = self.db.select("Users", myvars, \
			where="email=$email AND pass=$passwd")

		if len(ident) == 1:
			return True
		else:
			return False

	def addcourse(self, email, crn, term):
		if not self._checkcourse(email, crn, term):
			return False;

		self.db.insert("Courses", email = email, crn = crn, term = term)
		return True;
	
	def _checkcourse(self, email, crn, term):
		myvars = {'email': email, 'crn': crn, 'term': term}
		courses = self.db.select("Courses", myvars, \
			where="email=$email AND crn=$crn AND term=$term")

		if len(courses) != 0:
			return False
		else:
			return True

	def getcourses(self, email):
		courses = self.db.select("Courses", dict(email = email), \
			where="email=$email")
		return courses

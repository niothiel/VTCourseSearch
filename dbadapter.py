class DBAdapter:
	def __init__(self, db):
		self.db = db

	# TODO: Fix the fucking sql injection
	def login(self, email, passwd):
		args = {'email': email, 'passwd': passwd}
		ident = self.db.query("SELECT * FROM Users WHERE email='" + \
			email + "' AND pass='" + passwd + "'")

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
		courses = self.db.query("SELECT * FROM Courses WHERE email='%s' AND crn='%s' AND term='%s'" % (email, crn, term))
		if len(courses) != 0:
			return False
		else:
			return True

	def getcourses(self, email):
		courses = self.db.query("SELECT * FROM Courses WHERE email='%s'" % email)
		return courses

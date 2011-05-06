class DBAdapter:
	login = "SELECT * FROM Users WHERE email=$email AND pass=$passwd"

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

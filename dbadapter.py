import datetime
import hashlib
import pymongo
import shelve

'''
Data Layout:
	email
	passwd
	phone
	courses (list)
		crn
		term
		available

'''

class AbstractDBAdapter(object):
	def does_email_exist(self, email):
		raise TypeError('Not implemented.')

	def is_login_valid(self, email, passwd):
		raise TypeError('Not implemented.')

	def add_user(self, email, passwd, phone):
		raise TypeError('Not implemented.')

	def _course_exists(self, email, crn, term):
		raise TypeError('Not implemented.')

	def add_course(self, email, crn, term):
		raise TypeError('Not implemented.')

	def get_courses(self, email=None):
		raise TypeError('Not implemented.')

	def delete_course(self, email, crn, term):
		raise TypeError('Not implemented.')

	def hash_passwd(self, passwd):
		# Salted SHA-1 hashing of passwords.
		hashobj = hashlib.sha1()
		hashobj.update('vtcs')
		hashobj.update(passwd)
		return hashobj.hexdigest()

class MongoDBAdapter(AbstractDBAdapter):
	def __init__(self, host=None, port=None):
		super(MongoDBAdapter, self).__init__()
		self.connection = pymongo.MongoClient(host, port)
		self.db = self.connection.vtcs.data

	def does_email_exist(self, email):
		return self._get_row(email) is not None

	def is_login_valid(self, email, passwd):
		query = {
			'email': email,
			'passwd': self.hash_passwd(passwd)
		}
		return self.db.find_one(query) is not None

	def add_user(self, email, passwd, phone):
		row = {
			'email': email,
			'passwd': self.hash_passwd(passwd),
			'courses': [],
			'phone': phone
		}
		self.db.insert(row)

	def _course_exists(self, email, crn, term):
		query = {
			'email': email,
			'courses': {
				'$elemMatch': {
					'crn': crn,
				    'term': term
				}
			}
		}
		print 'Printing result from course existance'
		for a in self.db.find(query):
			print a
		return self.db.find_one(query) is not None

	def _get_row(self, email):
		return self.db.find_one({'email': email})

	def add_course(self, email, crn, term):
		crn = int(crn)
		term = int(term)

		if self._course_exists(email, crn, term):
			print 'Course Exists!'
			return False

		update_data = {
			'$push': {
				'courses': {
					'crn': crn,
				    'term': term,
				    'available': False,
				    'timeadded': datetime.datetime.now()
				}
			}
		}

		print self.db.update({'email': email}, update_data)
		return True

	def get_courses(self, email=None):
		if email is not None:
			row = self.db.find_one({'email': email})
			if row is not None:
				return row['courses']
			return []

		result = []

		for row in self.db.find():
			result.append(row['courses'])
		return result

	def delete_course(self, email, crn, term):
		if not self._course_exists(email, crn, term):
			return False

		# Pulling the entry, modify it, then saving it back
		row = self._get_row(email)

		# TODO: There has to be a better way to remove a specific element from a list...
		to_remove = None
		for course in row['courses']:
			if course['crn'] == crn and course['term'] == term:
				to_remove = course
				break

		if to_remove is None:
			return False

		row['courses'].remove(to_remove)
		self.db.save(row)


class ShelfDBAdapter(AbstractDBAdapter):
	def __init__(self, file_name='data.db'):
		self.db = shelve.open(file_name, writeback=True)

	def does_email_exist(self, email):
		email = str(email)

		return email in self.db.keys()

	def is_login_valid(self, email, passwd):
		email = str(email)
		passwd = str(passwd)

		if not self.does_email_exist(email):
			return False

		if passwd == self.db[email]['passwd']:
			return True

		return False

	def add_user(self, email, passwd, phone):
		email = str(email)
		passwd = str(passwd)

		if self.does_email_exist(email):
			return False

		self.db[email] = {
			'passwd': passwd,
		    'courses': [],
		    'phone': phone,
		}
		self.db.sync()

	def _course_exists(self, email, crn, term):
		email = str(email)
		crn = int(crn)
		term = int(term)

		for course in self.db[email]['courses']:
			if crn == course['crn'] and term == course['term']:
				return True

		return False

	def add_course(self, email, crn, term):
		email = str(email)
		crn = int(crn)
		term = int(term)

		if self._course_exists(email, crn, term):
			print 'Course already exists!'
			return False

		course = {
			'crn': crn,
		    'term': term,
		    'available': False,
		    'timeadded': datetime.datetime.now()
		}
		self.db[email]['courses'].append(course)
		self.db.sync()
		return True

	def get_courses(self, email=None):
		email = str(email)

		if email is None:
			result = []
			for courses in self.db.values()['courses']:
				result.append(courses)
			return result

		return self.db[email]['courses']

	def delete_course(self, email, crn, term):
		email = str(email)
		crn = int(crn)
		term = int(term)

		if not self._course_exists(email, crn, term):
			return False

		new_list = []
		for course in self.db[email]['courses']:
			if not (int(course['crn']) == int(crn)) and course['term'] == term:
				new_list.append(course)

		self.db[email]['courses'][:] = new_list
		self.db.sync()
		return True
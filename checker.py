from csadapter import CSAdapter
from dbadapter import MongoDBAdapter
from notifier import Notifier

# Separate file that's meant to run as a daemon to update the mongo db
def update_availability(cs, db, notifier, email=None):
	print 'Started checks for availability....'

	if email is None:
		resultset = db.db.find()
	else:
		resultset = db.db.find({'email': email})

	for row in resultset:
		print 'Email:', row['email']
		for course in row['courses']:
			if not course['available']:
				term = course['term']
				crn = course['crn']
				print 'Checking course: Crn:', crn, 'Term:', term
				course['available'] = avail = cs.crn_available(term, crn)
				db.db.save(row)

				if avail:
					print 'It\'s available!'
					notifier.send_text(row['phone'], crn)
				else:
					print 'Still not available....'

def main():
	cs = CSAdapter()
	db = MongoDBAdapter()
	notifier = Notifier()

	update_availability(cs, db, notifier)

if __name__ == '__main__':
	main()
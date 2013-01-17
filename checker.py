from csadapter import CSAdapter
from dbadapter import MongoDBAdapter
from notifier import Notifier
import datetime
import time

# Separate file that's meant to run as a daemon to update the mongo db
def check_availability(cs, db, notifier, email=None):
	print datetime.datetime.now(), 'Started checks for availability....'

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
				print 'Checking course: Crn:', crn, 'Term:', term, '... ',
				course['available'] = avail = cs.crn_available(term, crn)
				db.db.save(row)

				if avail:
					print 'Available!'
					notifier.send_text(row['phone'], crn)
				else:
					print 'Still not available...'

	print 'Done checking.'

def main():
	cs = CSAdapter()
	db = MongoDBAdapter()
	notifier = Notifier()

	# Check for availability every 15 minutes.
	# TODO: Perhaps make it a bit more intelligent and adjust the sleep time.
	while True:
		check_availability(cs, db, notifier)
		time.sleep(15 * 60)
		#time.sleep(30)

if __name__ == '__main__':
	main()
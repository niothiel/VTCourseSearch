import re
from lepl.apps.rfc3696 import Email

class Validator:
	def __init__(self):
		pass

	def crn(self, crn):
		success = True
		success &= crn.isDigit()
		success &= len(crn) == 5
		success &= crn[0] != '0'
		
		return success

	def email(self, email):
		return Email()(email)

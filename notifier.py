import smtplib
import googlevoice
from email.mime.text import MIMEText

class Notifier:
	def __init__(self):
		self.smtp_server = 'smtp.comcast.net'
		self.from_email = 'no-reply@vtcoursesearch.com'

		with open('gvoicelogin.txt', 'r') as fin:
			gvoice_email = fin.readline()
			gvoice_password = fin.readline()

			# TODO: Find a better way to initialize this.. sometimes it takes forever. Low priority.
			self.voice = googlevoice.Voice()
			self.voice.login(gvoice_email, gvoice_password)

	# TODO: Complete email notifications.. Maybe send email from a specifically-created gmail account.
	def send_email(self, email, crn):
		body = 'Your course, ' + str(crn) + ' seems to be available, snatch it quickly!'
		msg = MIMEText(body)
		msg['Subject'] = 'VTCourseSearch: Availability Notification'
		msg['From'] = self.from_email
		msg['To'] = email

		smtp = smtplib.SMTP(self.smtp_server)
		smtp.sendmail(self.from_email, [email], msg)
		smtp.close()

	def send_text(self, phone, crn):
		body = 'Your course: ' + str(crn) + ' is available!'
		self.voice.send_sms(phone, body)
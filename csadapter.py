import urllib
from bs4 import BeautifulSoup

mainurl = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_DispRequest"
searchurl = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest?CAMPUS=0&TERMYEAR=%s&CORE_CODE=AR%%25&SUBJ_CODE=%%25&SCHDTYPE=%%25&CRSE_NUMBER=&crn=%s&open_only=%s&BTN_PRESSED=FIND+class+sections&inst_name="

class CSAdapter:
	def __init__(self):
		self.terms = None
		pass

	def get_terms(self):
		if self.terms is None:
			# Welp, I don't feel like doing this anymore. It seems like the options html for terms are malformed.
			'''
			# Note, incomplete code.
			html = geturl(mainurl)
			soup = BeautifulSoup(html)

			termtag = soup(name='select', attrs={'name':'TERMYEAR'})[0]
			print 'Termtag:', termtag

			print termtag.option

			result = []
			option_tag = termtag(name='option')
			while option_tag is not None:
				entry = {
					'value': option_tag['value'],
				    'text': option_tag.text
				}
				result.append(entry)
				option_tag = option_tag(name='option')

			self.terms = result'''
			self.terms = [
				{'value': 201301, 'text': 'Spring Semester 2013'},
				{'value': 201306, 'text': 'Summer Session I 2013'},
				{'value': 201307, 'text': 'Summer Session II 2013'}
			]
		return self.terms

	def crn_exists(self, term, crn):
		url = searchurl % (term, crn, "")
		html = geturl(url)
		return 'NO SECTIONS FOUND FOR THIS INQUIRY' not in html

	def crn_available(self, term, crn):
		url = searchurl % (term, crn, "on")
		html = geturl(url)
		return 'NO SECTIONS FOUND FOR THIS INQUIRY' not in html

def geturl(url):
	return urllib.urlopen(url).read()

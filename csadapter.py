import urllib

mainurl = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_DispRequest"
searchurl = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest?CAMPUS=0&TERMYEAR=%s&CORE_CODE=AR%%25&SUBJ_CODE=%%25&SCHDTYPE=%%25&CRSE_NUMBER=&crn=%s&open_only=%s&BTN_PRESSED=FIND+class+sections&inst_name="

class CSAdapter:
	def __init__(self):
		self.terms = None
		pass

	def get_terms(self):
		if self.terms is None:
			# TODO: Dynamically pull this information.
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

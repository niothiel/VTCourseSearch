import urllib
from BeautifulSoup import BeautifulSoup

mainurl = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_DispRequest"
searchurl = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_ProcRequest?CAMPUS=0&TERMYEAR=%s&CORE_CODE=AR%%25&SUBJ_CODE=%%25&SCHDTYPE=%%25&CRSE_NUMBER=&crn=%s&open_only=on&BTN_PRESSED=FIND+class+sections&inst_name="

class CSAdapter:
	def __init__(self):
		pass

	def getTerms(self):
		html = geturl(mainurl)
		soup = BeautifulSoup(html)

		termtag = soup(name='select', attrs={'name':'TERMYEAR'})[0]

		result = []
		for tag in termtag(name='option'):
			entry = {}
			entry['value'] = tag['value']
			entry['text'] = tag.text
			result.append(entry)
		return result

	def crnExists(self, term, crn):
		return False

	def crnAvailable(self, term, crn):
		url = searchurl % (term, crn)
		html = geturl(url)
		soup = BeautifulSoup(html)

		ref = soup.find("table", {"class": "dataentrytable"})
		if ref == None or len(ref.contents) != 3:
			return False
		else:
			return True

def geturl(url):
		f = urllib.urlopen(url)
		html = f.read()
		return html

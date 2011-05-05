import urllib
from BeautifulSoup import BeautifulSoup

mainurl = "https://banweb.banner.vt.edu/ssb/prod/HZSKVTSC.P_DispRequest"

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
		return False

def geturl(url):
		f = urllib.urlopen(url)
		html = f.read()
		return html

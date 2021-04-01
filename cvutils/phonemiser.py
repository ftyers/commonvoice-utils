import re, os

class Phonemiser:
	"""
	>>> p = Phonemiser('ab')
	>>> p.phonemise('гӏапынхъамыз')
	'ʕapənqaməz'
	"""
	def __init__(self, lang):
		self.lang = lang

		try:
			self.load_data()
		except FileNotFoundError:
			print('[Phonemiser] Function not implemented')

	def load_data(self):
		self.lkp = {}
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/'
		fd = open(data_dir + self.lang + '/phon.tsv')
		line = fd.readline() # Skip the first line
		line = fd.readline()
		while line:
			row = line.strip('\n').split('\t')
			k = row[0].strip()	
			v = row[1].strip()	
			if k not in self.lkp:
				self.lkp[k] = []
			self.lkp[k].append(v)
			line = fd.readline()
		
	def maxmatch(self, token):
		token += ' '

		if token.strip() == '':
			return []

		dictionary = self.lkp.keys()
	
		for i in range(0, len(token)+1):
			firstWord = token[0:-i]
			remainder = token[-i:]
			if firstWord in dictionary:
				return [firstWord] + self.maxmatch(remainder)
	
		firstWord = token[0]
		remainder = token[1:]
	
		return [firstWord] + self.maxmatch(remainder)
	
	def phonemise(self, token):
		ks = list(self.lkp.keys())
		ks.sort(key=lambda x : len(x), reverse=True)
		segs = self.maxmatch(token.lower())	
		op = ''
		for seg in segs:
			if seg in self.lkp:
				op += self.lkp[seg][0]
		return op
	
if __name__ == "__main__":
	import doctest
	doctest.testmod()

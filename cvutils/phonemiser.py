import re, os, sys
from att import ATTFST
import pathlib

class Phonemiser:
	"""
	>>> p = Phonemiser('ab')
	>>> p.phonemise('гӏапынхъамыз')
	'ʕapənqaməz'
	>>> p = Phonemiser('lt')
	>>> p.phonemise('abažūras')
	'ɐbɐʒuːɾɐs̪'
	"""
	def __init__(self, lang):
		self.lang = lang
		self.transducer = None
		try:
			self.load_data()
		except FileNotFoundError:
			print('[Phonemiser] Function not implemented')

	def load_data(self):
		self.lkp = {}
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/' + self.lang + '/'
		paths = [p.name for p in pathlib.Path(data_dir).glob('phon.*')]
		if len(paths) == 0:
			raise FileNotFoundError
		for path in paths:
			if path.count('.att') > 0:
				self.load_data_att()
				break
			if path.count('.tsv') > 0:
				self.load_data_tsv()
				break

	def load_data_att(self):
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/' + self.lang + '/'
		self.transducer = ATTFST(data_dir + '/phon.att')	
		self.phonemise = self.lookup_att

	def load_data_tsv(self):
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/' + self.lang + '/'
		fd = open(data_dir + '/phon.tsv')
		line = fd.readline() # Skip the first line
		line = fd.readline()
		while line:
			row = line.strip('\n').split('\t')
			k = row[0].strip()	
			v = row[1].strip()	
			if v == '_':
				v = ''
			if k not in self.lkp:
				self.lkp[k] = []
			self.lkp[k].append(v)
			line = fd.readline()
		self.phonemise = self.lookup_tsv
		
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

	def lookup_att(self, token):
		res = list(self.transducer.apply(token))
		if len(res) > 0:
			return res[0][0]
		return None

	def lookup_tsv(self, token):
		ks = list(self.lkp.keys())
		ks.sort(key=lambda x : len(x), reverse=True)
		segs = self.maxmatch(token.lower())	
		op = ''
		for seg in segs:
			if seg in self.lkp:
				op += self.lkp[seg][0]
		return op
	
	def phonemise(self, token):
		if self.transducer:
			self.lookup_att(token)
		elif len(self.lkp.keys()) > 0:
			self.lookup_tsv(token)
		return None	

if __name__ == "__main__":
	import doctest
	doctest.testmod()

import re, os, sys
from att import ATTFST
import pathlib
from validator import Validator

class Transliterator:
	"""
	>>> p = Transliterator('sr')
	>>> p.transliterate('ћирилица')
	'ćirilica'
	>>> p.transliterate('ćirilica')
	'ћирилица'
	"""
	def __init__(self, lang, normalise=True):
		self.lang = lang
		self.detector = {}
		self.transducer = None
		self.normalise = None
		try:
			self.load_data()
		except FileNotFoundError:
			print('[Transliterator] Function not implemented', file=sys.stderr)
		try:
			self.validator = Validator(self.lang)
		except FileNotFoundError:
			pass
		if self.validator and normalise:
			self.normalise = self.validator.normalise

	def load_data(self):
		self.lkp = {}
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/' + self.lang + '/'
		paths = [p.name for p in pathlib.Path(data_dir).glob('transliterate.*')]
		if len(paths) == 0:
			raise FileNotFoundError
		for path in paths:
		#	if path[-4:] == '.att':
		#		self.load_data_att()
		#		break
			if path[-4:] == '.tsv':
				self.load_data_tsv()
				break

	#def load_data_att(self):
	#	data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/' + self.lang + '/'
	#	self.transducer = ATTFST(data_dir + '/phon.att')	
	#	self.transliterate = self.lookup_att

	def load_data_tsv(self):
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/' + self.lang + '/'
		fd = open(data_dir + '/transliterate.tsv')
		# Cyrl	Latn
		scripts_row = fd.readline().strip().split('\t') 
		# [а-я]	[a-z]
		detector_row = fd.readline().strip().split('\t') 

		a2b = scripts_row[0] + '-' + scripts_row[1]
		b2a = scripts_row[1] + '-' + scripts_row[0]
			
		self.detector[detector_row[0]] = a2b
		self.detector[detector_row[1]] = b2a

		self.lkp[a2b] = {}
		self.lkp[b2a] = {}

		line = fd.readline()
		while line:
			row = line.strip('\n').split('\t')
			k = row[0].strip('\n ')	
			v = row[1].strip('\n ')	
			if v == '_':
				v = ''
			if k not in self.lkp[a2b]:
				self.lkp[a2b][k] = []
			if k.upper() not in self.lkp[a2b]:
				self.lkp[a2b][k.upper()] = []
			if k.title() not in self.lkp[a2b]:
				self.lkp[a2b][k.title()] = []
			if v not in self.lkp[b2a]:
				self.lkp[b2a][v] = []
			if v.upper() not in self.lkp[b2a]:
				self.lkp[b2a][v.upper()] = []
			if v.title() not in self.lkp[b2a]:
				self.lkp[b2a][v.title()] = []
			self.lkp[a2b][k].append(v)
			self.lkp[b2a][v].append(k)
			self.lkp[a2b][k.upper()].append(v.upper())
			self.lkp[b2a][v.upper()].append(k.upper())
			self.lkp[a2b][k.title()].append(v.title())
			self.lkp[b2a][v.title()].append(k.title())
			line = fd.readline()
		self.transliterate = self.lookup_tsv
		
	def maxmatch(self, token, dictionary):
		token += ' '

		if token.strip() == '':
			return []

	
		for i in range(0, len(token)+1):
			firstWord = token[0:-i]
			remainder = token[-i:]
			if firstWord in dictionary:
				return [firstWord] + self.maxmatch(remainder, dictionary)
	
		firstWord = token[0]
		remainder = token[1:]
	
		return [firstWord] + self.maxmatch(remainder, dictionary)

#	def lookup_att(self, token):
#		if self.normalise:
#			token = self.normalise(token)[1]
#		res = list(self.transducer.apply(token))
#		if len(res) > 0:
#			return res[0][0]
#		return None

	def detect_script(self, token):
		which = ''
		max_which = 0
		for k in self.detector.keys():
			a = len(re.findall(k, token))
			if a >= max_which:
				max_which = a	
				which = k

		return self.detector[which]

	def lookup_tsv(self, token):
		direction = self.detect_script(token)	
#		print(direction)
#		print(self.lkp[direction])
#		print(self.normalise)
#		print(token)
		if self.normalise:
			token = self.normalise(token)[1]
		ks = list(self.lkp[direction].keys())
		ks.sort(key=lambda x : len(x), reverse=True)
		segs = self.maxmatch(token, ks)
		#print(segs)
		op = ''
		for seg in segs:
			if seg in self.lkp[direction]:
				op += self.lkp[direction][seg][0]
			else:
				op += seg
		return op

if __name__ == "__main__":
	import doctest
	doctest.testmod()

import re, os, sys, unicodedata

class Validator:
	"""
	>>> p = Validator('ab')
	>>> p.validate('Аллаҳ хаҵеи-ԥҳәыси иеилыхны, аҭыԥҳацәа роума иалихыз?')
	'аллаҳ хаҵеи-ԥҳәыси иеилыхны аҭыԥҳацәа роума иалихыз'
	"""
	def __init__(self, lang):
		self.lang = lang
		self.lower = False
		self.nfkc = False
		self.nfkd = False
		try:
			self.load_data()
		except FileNotFoundError:
			print('[Validator] Function not implemented', file=sys.stderr)

	def load_data(self):
		# Should probably remove this for langs that don't write space
		self.alphabet = [' '] 
		self.skip = [] 
		self.transform = {}
		self.lower = False
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/'
		for line in open(data_dir + self.lang + '/validate.tsv').readlines():
			if line[0] == '#':
				continue
			row = line.strip('\n').split('\t')
			if row[0] == 'ALLOW':
				a = row[1].strip()
				if a == '_':
					self.alphabet.append(' ')
				else:
					self.alphabet.append(a)
			if row[0] == 'LOWER':
				self.lower = True
			if row[0] == 'NFKC':
				self.nfkc = True
			if row[0] == 'NFKD':
				self.nfkd = True
			if row[0] == 'SKIP':
				self.skip.append(row[1])
			if row[0] == 'REPL' or row[0] == 'NORM' or row[0] == 'DEL':
				k = row[1].strip()
				v = row[2].strip()
				if row[2] == '_' and row[0] == 'REPL':
					self.transform[k] = ' '
				elif row[2] == '_' and row[0] == 'DEL':
					self.transform[k] = ''
				else:
					self.transform[k] = v
			# Remove all soft-hyphens, this should be safe cross-linguistically
			self.transform['\u00ad'] = ''
		#print('T:', self.transform, file=sys.stderr)

	def set_alphabet(s):
		self.alphabet = s

	def validate(self, transcript):
		"""Returns either the normalised transcript or None"""
		label = transcript.strip()
		if self.lower:
			label = label.lower()
		if self.nfkc:
			label = unicodedata.normalize('NFKC', label)
		if self.nfkd:
			label = unicodedata.normalize('NFKD', label)
		for k in self.transform:
			label = label.replace(k, self.transform[k])		
		for c in label:
			if c in self.skip:
				return None
			if c not in self.alphabet:
				return None

		label = re.sub('  *', ' ', label)
		label = label.strip()

		return label if label else None

	def normalise(self, transcript):
		"""Returns transcript and a flag to say if it passes or not"""
		label = transcript.strip()
		if self.lower:
			label = label.lower()
		if self.nfkc:
			label = unicodedata.normalize('NFKC', label)
		if self.nfkd:
			label = unicodedata.normalize('NFKD', label)
		for k in self.transform:
			label = label.replace(k, self.transform[k])		
			#print('K:', k, label, file=sys.stderr)

		for c in label:
			#print('c:', c, '%04x' % ord(c))
			if c in self.skip:
				return (False, label)
			if c not in self.alphabet:
				#print('X',c, '%04x' %ord(c))
				return (False, label)

		label = re.sub('  *', ' ', label)
		label = label.strip()

		return (True, label) if label else (False, label)

	def check(self, transcript):
		"""Finds the non-alphabetic characters in a transcript"""
		label = transcript.strip()
		if self.lower:
			label = label.lower()
		if self.nfkc:
			label = unicodedata.normalize('NFKC', label)
		if self.nfkd:
			label = unicodedata.normalize('NFKD', label)
		for k in self.transform:
			label = label.replace(k, self.transform[k])		
		unalphabetic = set()
		skipped = False
		for c in label:
			if c in self.skip:
				skipped = True
				break
			if c not in self.alphabet:
				unalphabetic.add(c)
		
		return (skipped, unalphabetic)


if __name__ == "__main__":
	import doctest
	doctest.testmod()


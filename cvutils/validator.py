import re, os, sys

class Validator:
	"""
	>>> p = Validator('ab')
	>>> p.validate('Аллаҳ хаҵеи-ԥҳәыси иеилыхны, аҭыԥҳацәа роума иалихыз?')
	'аллаҳ хаҵеи-ԥҳәыси иеилыхны аҭыԥҳацәа роума иалихыз'
	"""
	def __init__(self, lang):
		self.lang = lang

		try:
			self.load_data()
		except FileNotFoundError:
			print('[Validator] Function not implemented')

	def load_data(self):
		self.alphabet = [' '] 
		self.skip = [] 
		self.transform = {}
		self.lower = False
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/'
		for line in open(data_dir + self.lang + '/validate.tsv').readlines():
			row = line.strip('\n').split('\t')
			if row[0] == 'ALLOW':
				a = row[1].strip()
				if a == '_':
					self.alphabet.append(' ')
				else:
					self.alphabet.append(a)
			if row[0] == 'LOWER':
				self.lower = True
			if row[0] == 'SKIP':
				self.skip.append(row[1])
			if row[0] == 'REPL' or row[0] == 'NORM':
				k = row[1].strip()
				v = row[2].strip()
				if row[2] == '_':
					self.transform[k] = ' '
				else:
					self.transform[k] = v

	def set_alphabet(s):
		self.alphabet = s

	def validate(self, transcript):
		label = transcript
		if self.lower:
			label = label.lower()
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

if __name__ == "__main__":
	import doctest
	doctest.testmod()


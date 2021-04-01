import re

class Validator:
	"""
	>>> p = Validator('ab')
	>>> p.validate('Аллаҳ хаҵеи-ԥҳәыси иеилыхны, аҭыԥҳацәа роума иалихыз?')
	'аллаҳ хаҵеи-ԥҳәыси иеилыхны аҭыԥҳацәа роума иалихыз'
	"""
	def __init__(self, lang):
		self.lang = lang

		self.load_data()

	def load_data(self):
		self.alphabet = [] 
		self.transform = {}
		self.lower = False
		for line in open('data/' + self.lang + '/validate.tsv').readlines():
			row = line.strip('\n').split('\t')
			if row[0] == 'ALLOW':
				a = row[1].strip()
				if a == '_':
					self.alphabet.append(' ')
				else:
					self.alphabet.append(a)
			if row[0] == 'LOWER':
				self.lower = True
			if row[0] == 'REPL':
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
			if c not in self.alphabet:
				return None

		label = re.sub('  *', ' ', label)
		label = label.strip()

		return label if label else None

if __name__ == "__main__":
	import doctest
	doctest.testmod()


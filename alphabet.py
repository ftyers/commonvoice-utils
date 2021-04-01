class Alphabet:
	"""
	>>> p = Alphabet('ab')
	>>> p.get_alphabet()
	'абвгдежзийклмнопрстуфхцчшщъыьэюяёӏ'
	"""
	def __init__(self, lang):
		self.lang = lang
		self.load_data()

	def load_data(self):
		a = [line.strip('\n') for line in open('data/' + self.lang + '/alphabet.txt').readlines()]
		a = list(set(''.join(a)))
		a.sort()
		self.alphabet = ''.join(a)

	def get_alphabet(self):
		return self.alphabet


if __name__ == "__main__":
        import doctest
        doctest.testmod()


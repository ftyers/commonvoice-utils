import os

class Alphabet:
	"""
	>>> p = Alphabet('ab')
	>>> p.get_alphabet()
	'абвгдежзийклмнопрстуфхцчшщъыьэюяёӏ'
	"""
	def __init__(self, lang):
		self.lang = lang
		try:
			self.load_data()
		except FileNotFoundError:
			print('[Alphabet] Function not implemented')

	def load_data(self):
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/'
		fd = open(data_dir + self.lang + '/alphabet.txt')
		a = [' '] + [line.strip('\n') for line in fd.readlines()]
		a = list(set(''.join(a)))
		a.sort()
		self.alphabet = ''.join(a)

	def get_alphabet(self):
		return self.alphabet


if __name__ == "__main__":
        import doctest
        doctest.testmod()


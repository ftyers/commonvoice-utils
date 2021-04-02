import os

class Corpus:
	"""
	>>> c = Corpus('sah')
	>>> c.dump_url()
	'https://dumps.wikimedia.org/sahwiki/latest/sahwiki-latest-pages-articles.xml.bz2'
	>>> c = Corpus('cv')
	>>> c.target_segments()
	['пӗрре','иккӗ','виҫҫӗ','тӑваттӑ','пиллӗк','улттӑ','ҫиччӗ','саккӑр','тӑххӑр','вуннӑ','ҫапла','ҫук']
	"""
	def __init__(self, lang):
		self.lang = lang
		try:
			self.load_data()
		except FileNotFoundError:
			print('[Corpus] Function not implemented')

	def load_data(self):
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/'
		fd = open(data_dir + self.lang + '/vocab.tsv')
		self.small_vocab = [line.strip('\n') for line in fd.readlines()]

	def target_segments(self):
		return self.small_vocab

	def dump_url(self):
		return 'https://dumps.wikimedia.org/%swiki/latest/%swiki-latest-pages-articles.xml.bz2' % (self.lang, self.lang)


if __name__ == "__main__":
        import doctest
        doctest.testmod()


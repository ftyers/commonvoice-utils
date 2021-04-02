import os

class Corpora:
	"""
	>>> c = Corpora('sah')
	>>> c.dump_url()
	'https://dumps.wikimedia.org/sahwiki/latest/sahwiki-latest-pages-articles.xml.bz2'
	>>> c = Corpora('cv')
	>>> c.target_segments()
	['пӗрре', 'иккӗ', 'виҫҫӗ', 'тӑваттӑ', 'пиллӗк', 'улттӑ', 'ҫиччӗ', 'саккӑр', 'тӑххӑр', 'вуннӑ', 'ҫапла', 'ҫук']
	>>> c = Corpora('ga-IE')
	>>> c.dump_url()
	'https://dumps.wikimedia.org/gawiki/latest/gawiki-latest-pages-articles.xml.bz2'
	>>> c = Corpora('kpv')
	>>> c.dump_url()
	'https://dumps.wikimedia.org/kvwiki/latest/kvwiki-latest-pages-articles.xml.bz2'
	>>> c = Corpora('quc')
	>>> c.dump_url()
	>>> c = Corpora('rm-vallader')
	>>> c.dump_url()
	'https://dumps.wikimedia.org/rmwiki/latest/rmwiki-latest-pages-articles.xml.bz2'
	"""
	def __init__(self, lang):
		self.lang = lang
		self.load_data()

	def load_data(self):
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/'
		vocab_file = data_dir + self.lang + '/vocab.tsv'
		self.small_vocab = []
		if os.path.isfile(vocab_file):
			fd = open(data_dir + self.lang + '/vocab.tsv')
			self.small_vocab = [line.strip('\n') for line in fd.read().strip().split('\n')]
		self.wikipedia_code = self.lang
		wikipedia_file = data_dir + self.lang + '/wikipedia.txt'
		if os.path.isfile(wikipedia_file):
			self.wikipedia_code = open(wikipedia_file).read().strip()

	def target_segments(self):
		return self.small_vocab

	def dump_url(self):
		if self.wikipedia_code:
			return 'https://dumps.wikimedia.org/%swiki/latest/%swiki-latest-pages-articles.xml.bz2' % (self.wikipedia_code, self.wikipedia_code)
		return None


if __name__ == "__main__":
        import doctest
        doctest.testmod()


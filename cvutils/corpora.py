import os, urllib.request, re

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

	def opus(self):
		"""Get a list of URLs from OPUS for a given language code"""
		q = 'https://opus.nlpl.eu/?src=' + self.lang + '&trg=en'
		p = urllib.request.urlopen(q)
		page = p.read().decode('utf-8').split('\n')
		d = ''
		area = False
		for line in page:
			if line.count('<b>Language resources: </b>'):
				area = True
			if line.count('</table>'):
				area = False  
			if area:
				d+= line

		if not d:
			return None

		urls = []
		for line in d.replace('<td>','\n<td>').split('\n'):
			urltitle = re.findall('href="[^"]+" title="[^"]+"', line)
# <td>&nbsp;<a rel="nofollow" href="https://object.pouta.csc.fi/OPUS-wikimedia/v20190628/smt/ab-en.alg.zip" title="1 aligned documents,58 sentence alignments">alg</a>&nbsp;<a rel="nofollow" href="https://object.pouta.csc.fi/OPUS-wikimedia/v20190628/smt/ab-en.zip" title="1 aligned documents,58 sentence alignments">smt</a>&nbsp;</td>
			for entry in urltitle:
				e = entry.replace('href="','').strip('"').split('" title="')
				if self.lang + '.txt.gz' in e[0] and '/mono/' in e[0]:
					urls.append(e)
		return urls					

	def filter(self, input_fd, output_fd, umbral=10):
		"""Apply a frequency filter to an input stream"""
		word2sent = {} # token -> sentence
		word2freq = {} # token -> frequency
		id2found = {} # sentence id -> number of words over the umbral
		id2len = {} # sentence id -> len in tokens
		id2sent = {} # sentence id -> sentence

		idx = 0
		for line in input_fd:
			id2sent[idx] = line.strip('\n')
			if idx not in id2found:
				id2found[idx] = 0
			# do better tokenisation
			tokens = id2sent[idx].split(' ') 
			id2len[idx] = len(tokens)
			#print('!!!', idx, tokens)
			flush = set()
			for token in tokens:
				if token not in word2freq:
					word2freq[token] = 0
				word2freq[token] += 1
				if token not in word2sent:
					word2sent[token] = set()
				word2sent[token].add(idx)	
				if word2freq[token] >= umbral:
					for sent in word2sent[token]:
						if sent in id2found:
							id2found[sent] += 1
					# mark the token for flushing
					flush.add(token)
			removed = set()
			for word in flush:
				for sent in word2sent[word]:
					if sent not in id2len or sent not in id2found:
						continue
					if id2len[sent] == id2found[sent]:
						#print('$$$', word2freq)
						#print('###', id2found[sent], '|||', id2len[sent])
						removed.add(sent)
				for sent in removed:
					if sent in word2sent[word]:
						word2sent[word].remove(sent)

			for sent in removed:
				print(id2sent[sent], file=output_fd)
				if sent in id2sent: del id2sent[sent]
				if sent in id2found: del id2found[sent]
				if sent in id2len: del id2len[sent]
			
			idx += 1

if __name__ == "__main__":
        import doctest
        doctest.testmod()


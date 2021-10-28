import os, urllib.request, re, sys

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
		self.opus_weights = {}
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
		for line in open(os.path.abspath(os.path.dirname(__file__))+'/opus.weights').readlines():
			(v, k, r) = line.strip().split('\t')
			self.opus_weights[k] = (int(v), r.split(','))

	def target_segments(self):
		return self.small_vocab

	def dump_url(self):
		if self.wikipedia_code:
			return 'https://dumps.wikimedia.org/%swiki/latest/%swiki-latest-pages-articles.xml.bz2' % (self.wikipedia_code, self.wikipedia_code)
		return None

	def opus(self):
		"""Get a list of URLs from OPUS for a given language code"""
		URL_BASE = 'https://object.pouta.csc.fi/'
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
					name = e[0].replace(URL_BASE, '')
					name = name.split('/')[0]
					w = 0
					r = []
					if name in self.opus_weights:
						w = self.opus_weights[name][0]
						r = self.opus_weights[name][1]
					urls.append((w, r, name, e))
		return urls					

	# TODO: We should allow a warm-up frequency list of 1-10k tokens
	def filter(self, input_fd, output_fd, umbral=10):
		"""Apply a frequency filter to an input stream"""
		word2sent = {} # A map of tokens to input line hashes
		word2freq = {} # A map of words to their frequencies so far
		hash2sent = {} # A map of line hashes to lists of tokens
		hash2line = {} # A map of line hashes to input lines
		output_lines = set() # Lines that have been output / seen, implicitly removes duplicates

		def tokenise(s):
			"""Basic tokenisation function"""
			return s.split(' ')

		def update_sentence(freqs, tokens, umbral):
			"""Update the tokens in the sentence that have not reached the umbral"""
			new_sent = set()	
			for token in tokens:
				if freqs[token] < umbral:
					new_sent.add(token)
			return new_sent 

		flush_tokens = set()
		flush_point = 1
		for line in input_fd:
			line = line.strip()
			line_hash = hash(line)
			if line_hash in output_lines:
				# If we have already seen the line, skip it
				continue
			tokens = tokenise(line)
			hash2line[line_hash] = line
			hash2sent[line_hash] = set(tokens)
			for token in tokens:
				if token not in word2freq: word2freq[token] = 0
				word2freq[token] += 1	
				if token not in word2sent: word2sent[token] = set()
				word2sent[token].add(line_hash)
			
				# If we find a token that exceeds the umbral, add it to the list
				# of tokens which we should check 
				if word2freq[token] >= umbral:
					flush_tokens.add(token)
			
			if len(flush_tokens) > flush_point:
				for token in flush_tokens:
					# The sentences for this token that have yet to make the umbral
					new_sents = set()
					for line_hash in word2sent[token]:
						# If the line has been output, skip it
						if line_hash in output_lines:
							continue
						# Check the sentence to see if all tokens are above the umbral
						hash2sent[line_hash] = update_sentence(word2freq, hash2sent[line_hash], umbral)
		
						if len(hash2sent[line_hash]) == 0:
							print(hash2line[line_hash], file=output_fd)
							output_lines.add(line_hash)
							del hash2line[line_hash]
							del hash2sent[line_hash]
							continue
						new_sents.add(line_hash)
					word2sent[token] = new_sents
				flush_tokens = set()
				flush_point = max(word2freq.values()) 
				print('flush_point:', flush_point, file=sys.stderr)

			# End of stream
			for token in flush_tokens:
				# The sentences for this token that have yet to make the umbral
				new_sents = set()
				for line_hash in word2sent[token]:
					# If the line has been output, skip it
					if line_hash in output_lines:
						continue
					# Check the sentence to see if all tokens are above the umbral
					hash2sent[line_hash] = update_sentence(word2freq, hash2sent[line_hash], umbral)
	
					if len(hash2sent[line_hash]) == 0:
						print(hash2line[line_hash], file=output_fd)
						output_lines.add(line_hash)
						del hash2line[line_hash]
						del hash2sent[line_hash]
						continue
					new_sents.add(line_hash)
				word2sent[token] = new_sents



if __name__ == "__main__":
        import doctest
        doctest.testmod()


import re, os

class Segmenter:
	"""
	>>> s = Segmenter('br')
	>>> s.segment("Peurliesañ avat e kemm ar vogalennoù e c'hengerioù evit dont da vezañ heñvel ouzh ar vogalennoù en nominativ (d.l.e. ar stumm-meneg), da skouer e hungareg: Aour, tungsten, zink, uraniom, h.a., a vez kavet e kondon Bouryatia. A-bouez-bras evit armerzh ar vro eo al labour-douar ivez pa vez gounezet gwinizh ha legumaj dreist-holl. A-hend-all e vez gounezet arc'hant dre chaseal ha pesketa.")
	["Peurliesañ avat e kemm ar vogalennoù e c'hengerioù evit dont da vezañ heñvel ouzh ar vogalennoù en nominativ (d.l.e. ar stumm-meneg), da skouer e hungareg: Aour, tungsten, zink, uraniom, h.a., a vez kavet e kondon Bouryatia.", 'A-bouez-bras evit armerzh ar vro eo al labour-douar ivez pa vez gounezet gwinizh ha legumaj dreist-holl.', "A-hend-all e vez gounezet arc'hant dre chaseal ha pesketa."]
	"""
	def __init__(self, lang):
		self.lang = lang

		try:
			self.load_data()
		except FileNotFoundError:
			print('[Segmenter] Function not implemented')

	def load_data(self):
		self.eos = []
		data_dir = os.path.abspath(os.path.dirname(__file__)) + '/data/'
		for line in open(data_dir + self.lang + '/validate.tsv').readlines():
			row = line.strip('\n').split('\t')
			if row[0] == 'NORM':
				k = row[1].strip()	
				v = row[2].strip()	
				self.transform[k] = v
		for line in open(data_dir + self.lang + '/punct.tsv').readlines():
			row = line.strip('\n').split('\t')
			k = row[1].strip()	
			self.eos.append(k)
		self.abbr = []
		for line in open(data_dir + self.lang + '/abbr.tsv').readlines():
			row = line.strip('\n').split('\t')
			k = row[1].strip()	
			self.abbr.append(k)

	def normalise(self, s):
		o = s
		for ch in self.transform:
			o = o.replace(ch, self.transform[ch])
		return o
				
	def segment(self, paragraph, normalise=False):
		sentences = []

		if normalise:
			paragraph = self.normalise(paragraph)

		tokens = paragraph.replace(' ', ' ¶ ').split(' ')
		sentence = ''
		for token in tokens:
			token = token.strip()
			if not token:
				continue
			if token == '¶':
				sentence += ' '
				continue
			if token[-1] in self.eos:
				if re.match('\W*(' + '|'.join(self.abbr) + ')\W*', token):
					sentence += token
				else: 
					sentence += token
					sentences.append(sentence.strip())
					sentence = ''
			else:
				sentence += token

		return sentences
	
if __name__ == "__main__":
	import doctest
	doctest.testmod()

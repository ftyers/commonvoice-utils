import re 


class Segmenter:
	"""
	>>> s = Segmenter('br')
	>>> s.segment("Peurliesañ avat e kemm ar vogalennoù e c'hengerioù evit dont da vezañ heñvel ouzh ar vogalennoù en nominativ (d.l.e. ar stumm-meneg), da skouer e hungareg: Aour, tungsten, zink, uraniom, h.a., a vez kavet e kondon Bouryatia. A-bouez-bras evit armerzh ar vro eo al labour-douar ivez pa vez gounezet gwinizh ha legumaj dreist-holl. A-hend-all e vez gounezet arc'hant dre chaseal ha pesketa.")
	["Peurliesañ avat e kemm ar vogalennoù e c'hengerioù evit dont da vezañ heñvel ouzh ar vogalennoù en nominativ (d.l.e. ar stumm-meneg), da skouer e hungareg: Aour, tungsten, zink, uraniom, h.a., a vez kavet e kondon Bouryatia.", 'A-bouez-bras evit armerzh ar vro eo al labour-douar ivez pa vez gounezet gwinizh ha legumaj dreist-holl.', "A-hend-all e vez gounezet arc'hant dre chaseal ha pesketa."]
	"""
	def __init__(self, lang):
		self.lang = lang

		self.load_data()

	def load_data(self):
		self.eos = []
		for line in open('data/' + self.lang + '/punct.tsv').readlines():
			row = line.strip('\n').split('\t')
			k = row[1].strip()	
			self.eos.append(k)
		self.abbr = []
		for line in open('data/' + self.lang + '/abbr.tsv').readlines():
			row = line.strip('\n').split('\t')
			k = row[1].strip()	
			self.abbr.append(k)
				
	def segment(self, paragraph):
		sentences = []

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

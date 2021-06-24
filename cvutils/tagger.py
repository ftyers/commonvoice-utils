"""Grammatical tagging for sentences."""
import re

"""
	FIXME:
		- Put rules in linguistic data files
		- Tag other POS
"""

class Tagger:

	def __init__(self, lang):
		self.tag = self._default

		if lang in ["de", "deu"]:
			self.tag = self._deu
		if lang in ["ja", "jpn"]:
			self.tag = self._jpn
		
	def _deu(self, sentence):
		"""Convert deu sentences to tags.
	
		>>> deu(['Ich', 'habe', 'schlechte', 'Nachrichten', 'für', 'ihn', '.'])
		['X', 'X', 'X', 'X', 'X', 'X', 'PUNCT']
		"""
		tags = []
		for token in sentence:
			if re.match(r"^[^\w+]+$", token):
				tags.append("PUNCT")
			else:
				tags.append("X")
	
		return tags
	
	def _jpn(self, sentence):
		"""Convert jpn sentences to tags.
	
		>>> _jpn(['切手', 'を', '十', '枚', 'と', 'はがき', 'を', '三', '枚', '買い', 'ます', '。'])
		['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'PUNCT']
		"""
		tags = []
		for token in sentence:
			if re.match(r"^[^\w+]+$", token):
				tags.append("PUNCT")
			else:
				tags.append("X")
	
		return tags
	
	def _default(self, sentence):
		"""Defaut tags for sentences.
	
		>>> _default(['This', 'is', 'not', 'Crewe', '.'])
		['X', 'X', 'X', 'PROPN', 'PUNCT']
		"""
		tags = []
		first = True
		for token in sentence:
			if re.match(r"^\W+$", token):
				tags.append("PUNCT")
			elif token[0] == token[0].upper() and not first:
				tags.append("PROPN")
			else:
				tags.append("X")
			first = False
	
		return tags
	

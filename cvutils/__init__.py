import sys, os, pathlib, re

sys.path.append(os.path.dirname(__file__))

from phonemiser import Phonemiser
from segmenter import Segmenter
from validator import Validator
from alphabet import Alphabet
from corpora import Corpora
from transliterator import Transliterator
from tokeniser import Tokeniser
from tagger import Tagger
from gutenberg import Gutenberg

# This is horrible, rewrite this

class CV:
	def __init__(self):
		self.supported = {'phonemiser':[], 'segmenter':[], 'validator':[], 'alphabet':[]}

		data_dir = os.path.dirname(__file__) + '/data/'
		for path in pathlib.Path(data_dir).rglob('alphabet.txt'):
			locale = path.resolve()
			locale = str(locale).replace('/alphabet.txt', '').split('/')[-1]
			self.supported['alphabet'].append(locale)

		for path in pathlib.Path(data_dir).rglob('validate.tsv'):
			locale = path.resolve()
			locale = str(locale).replace('/validate.tsv', '').split('/')[-1]
			self.supported['validator'].append(locale)

		for path in pathlib.Path(data_dir).rglob('phon.*'):
			locale = path.resolve()
			if '.att' not in str(locale) and '.tsv' not in str(locale):
				continue
			locale = re.sub('/phon.(att|tsv)', '', str(locale)).split('/')[-1]
			self.supported['phonemiser'].append(locale)
	
		for path in pathlib.Path(data_dir).rglob('punct.tsv'):
			locale = path.resolve()
			locale = str(locale).replace('/punct.tsv', '').split('/')[-1]
			self.supported['segmenter'].append(locale)
							
				
	def alphabets(self):
		return self.supported['alphabet']

	def validators(self):
		return self.supported['validator']

	def phonemisers(self):
		return self.supported['phonemiser']

	def segmenters(self):
		return self.supported['segmenter']


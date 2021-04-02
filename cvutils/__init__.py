import sys, os, pathlib

sys.path.append(os.path.dirname(__file__))

from phonemiser import Phonemiser
from segmenter import Segmenter  
from validator import Validator
from alphabet import Alphabet

# This is horrible, rewrite this

class CV:
	def __init__(self):
		self.supported = {'phonemiser':[], 'segmenter':[], 'validator':[], 'alphabet':[]}

		for path in pathlib.Path(os.path.dirname(__file__) + '/data/').rglob('alphabet.txt'):
			locale = path.resolve()
			locale = str(locale).replace('/alphabet.txt', '').split('/')[-1]
			self.supported['alphabet'].append(locale)

		for path in pathlib.Path(os.path.dirname(__file__) + '/data/').rglob('validate.tsv'):
			locale = path.resolve()
			locale = str(locale).replace('/validate.tsv', '').split('/')[-1]
			self.supported['validator'].append(locale)
				
	def alphabet_available(self, code): 
		if code in self.supported['alphabet']:
			return True
		return False

	def validator_available(self, code): 
		if code in self.supported['validator']:
			return True
		return False


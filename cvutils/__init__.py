"""commonvoice-utils main module"""
import sys
import os
import pathlib

from .phonemiser import Phonemiser
from .segmenter import Segmenter
from .validator import Validator
from .alphabet import Alphabet
from .corpora import Corpora
from .transliterator import Transliterator
from .tokeniser import Tokeniser
from .tagger import Tagger
from .gutenberg import Gutenberg

# This is horrible, rewrite this
sys.path.append(os.path.dirname(__file__))

class CV:
    """Class to access supported functionality for locales"""
    def __init__(self):
        self.supported = {
            "phonemiser": [],
            "segmenter": [],
            "validator": [],
            "alphabet": [],
        }

        data_dir = os.path.join(os.path.dirname(__file__), "data")
        for path in pathlib.Path(data_dir).rglob("alphabet.txt"):
            locale = str(path.resolve())
            locale = os.path.split(os.path.split(locale)[0])[-1]
            self.supported["alphabet"].append(locale)

        for path in pathlib.Path(data_dir).rglob("validate.tsv"):
            locale = str(path.resolve())
            locale = os.path.split(os.path.split(locale)[0])[-1]
            self.supported["validator"].append(locale)

        for path in pathlib.Path(data_dir).rglob("phon.*"):
            locale = str(path.resolve())
            if ".att" not in locale and ".tsv" not in locale:
                continue
            locale = os.path.split(os.path.split(locale)[0])[-1]
            self.supported["phonemiser"].append(locale)

        for path in pathlib.Path(data_dir).rglob("punct.tsv"):
            locale = str(path.resolve())
            locale = os.path.split(os.path.split(locale)[0])[-1]
            self.supported["segmenter"].append(locale)

    def alphabets(self):
        """Returns a list of all language codes supporting the Alphabet fuctionality"""
        return self.supported["alphabet"]

    def validators(self):
        """Returns a list of all language codes supporting the Validator fuctionality"""
        return self.supported["validator"]

    def phonemisers(self):
        """Returns a list of all language codes supporting the Phonemizer fuctionality"""
        return self.supported["phonemiser"]

    def segmenters(self):
        """Returns a list of all language codes supporting the Segmenter fuctionality"""
        return self.supported["segmenter"]

"""Segmenter module"""
import os
import sys
import re


class Segmenter:
    """
    >>> s = Segmenter('br')
    >>> s.segment("Peurliesañ avat e kemm ar vogalennoù e c'hengerioù evit dont da vezañ heñvel ouzh ar vogalennoù en nominativ (d.l.e. ar stumm-meneg), da skouer e hungareg: Aour, tungsten, zink, uraniom, h.a., a vez kavet e kondon Bouryatia. A-bouez-bras evit armerzh ar vro eo al labour-douar ivez pa vez gounezet gwinizh ha legumaj dreist-holl. A-hend-all e vez gounezet arc'hant dre chaseal ha pesketa.")
    ["Peurliesañ avat e kemm ar vogalennoù e c'hengerioù evit dont da vezañ heñvel ouzh ar vogalennoù en nominativ (d.l.e. ar stumm-meneg), da skouer e hungareg: Aour, tungsten, zink, uraniom, h.a., a vez kavet e kondon Bouryatia.", 'A-bouez-bras evit armerzh ar vro eo al labour-douar ivez pa vez gounezet gwinizh ha legumaj dreist-holl.', "A-hend-all e vez gounezet arc'hant dre chaseal ha pesketa."]
    """

    def __init__(self, lang, quiet=False):
        self.lang = lang
        self.transform = {}

        try:
            self.load_data()
        except FileNotFoundError:
            if not quiet:
                print(
                    "[Segmenter] Function not implemented for {lang}", file=sys.stderr
                )
            sys.exit(-1)

    def load_data(self):
        self.eos = []
        data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")
        for line in open(
            os.path.join(data_dir, self.lang, "validate.tsv"), encoding="utf8"
        ).readlines():
            row = line.strip("\n").split("\t")
            if row[0] == "NORM":
                k = row[1].strip()
                v = row[2].strip()
                self.transform[k] = v
        for line in open(
            os.path.join(data_dir, self.lang, "punct.tsv"), encoding="utf8"
        ).readlines():
            row = line.strip("\n").split("\t")
            k = row[1].strip()
            self.eos.append(k)
        self.abbr = []
        for line in open(
            os.path.join(data_dir, self.lang, "abbr.tsv"), encoding="utf8"
        ).readlines():
            row = line.strip("\n").split("\t")
            k = row[1].strip()
            self.abbr.append(k.replace(".", "\\."))

    def normalise(self, s):
        o = s
        for ch in self.transform:
            o = o.replace(ch, self.transform[ch])
        return o

    def segment(self, paragraph, normalise=False):
        sentences = []

        if normalise:
            paragraph = self.normalise(paragraph)

        tokens = paragraph.replace(" ", " ¶ ").split(" ")
        sentence = ""
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            if token == "¶":
                sentence += " "
                continue
            if token[-1] in self.eos:
                # print(token)
                found = False
                for abbrev in self.abbr:
                    if re.match(r"\W*" + abbrev, token):
                        sentence += token
                        found = True
                        break

                if re.match("[0-9]+\.", token):
                    sentence += token
                elif not found:
                    sentence += token
                    sentences.append(sentence.strip())
                    sentence = ""
            else:
                sentence += token

        return sentences


if __name__ == "__main__":
    import doctest

    doctest.testmod()

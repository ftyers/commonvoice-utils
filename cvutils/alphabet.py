"""Alphabet module"""
import sys
import os


class Alphabet:
    """
    >>> p = Alphabet('ab')
    >>> p.get_alphabet()
    'абвгдежзийклмнопрстуфхцчшщъыьэюяёӏ'
    """

    def __init__(self, lang, quiet=False):
        self.lang = lang
        self.alphabet = ""
        try:
            self.load_data()
        except FileNotFoundError:
            if not quiet:
                print(
                    f"[Alphabet] Function not implemented for {lang}", file=sys.stderr
                )

    def load_data(self):
        data_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "data")
        fd = open(os.path.join(data_dir, self.lang, "alphabet.txt"), encoding="utf8")
        a = [" "] + [line.strip("\n") for line in fd.readlines()]
        a = list(set("".join(a)))
        a.sort()
        self.alphabet = "".join(a)

    def get_alphabet(self):
        return self.alphabet

    def write_alphabet(self, fn):
        fd = open(fn, "w", encoding="utf8")
        fd.write("".join([c + "\n" for c in self.alphabet]))
        fd.close()


if __name__ == "__main__":
    import doctest

    doctest.testmod()

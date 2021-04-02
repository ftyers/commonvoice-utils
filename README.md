# Common Voice Utils 

This repository collects together basic linguistic processing data for using dataset
dumps from the [Common Voice](commonvoice.mozilla.org/) project. It aims to provide a one-stop-shop for 
utilities and data useful in training ASR and TTS systems.

## Tools

* Phonemiser: 
  * A rudimentary grapheme to phoneme (g2p) system based on either:
    * a deterministic longest-match left-to-right replacement of orthographic units; or
    * a weighted finite-state transducer
* Validator: 
  * A validation script that can be used with `import_cv2.py` from [coqui-ai/STT](https://github.com/coqui-ai/STT/)
  * It checks a sentence to see if it can be converted and if possible normalises the encoding, removes punctuation and returns it
* Alphabet: 
  * The relevant alphabet of the language, appropriate for use in training ASR
* Segmenter: 
  * A deterministic sentence segmentation algorithm tuned for segmenting paragraphs from Wikipedia

## Language support 

| Language | Autonym   | Code | Code (CV) | Phon | Valid | Alphabet | Segment |
|--------------------- |---------- |----- |------- |----------- |----------|---------- |------------|
| Abaza                | Абаза     |`abq` | `ab`   | ✔          | ✔         | ✔        |           |
| Arabic               | اَلْعَرَبِيَّةُ     |`ara` | `ar`   |     —       |   ✔         |          ✔  |            |
| Assamese             |  অসমীয়া    |`asm` | `as`   |            |           |          |            |
| Basaa                | Basaa        |`bas` | `bas`   |     ✔      |          | ✔        |           |
| Breton               | Brezhoneg |`bre` | `br`   | ✔          | ✔         | ✔        |      ✔     |
| Catalan              | Català     |`cat` | `ca`   |            |           |      ✔    |            |
| Czech                | Čeština     |`ces` | `cs`   |    ✔        |    ✔        |  ✔        |            |
| Chuvash              | Чӑвашла |`chv` | `cv`   | ✔          | ✔         | ✔        |      ✔     |
| Hakha Chin           | Hakha Lai |`cnh` | `cnh`   |            |           |     ✔      |            |
| Welsh                | Cymraeg     |`cym` | `cy`   |       ✔      |           |     ✔      |            |
| Dhivehi              | ދިވެހި         |`div` | `dv`   | ✔          |        |      |         |
| Greek                | Ελληνικά |`ell` | `el`   | ✔          |        |  ✔      |         |
| German               | Deutsch     |`deu` | `de`   |            |          ✔  |     ✔      |            |
| English              | English     |`eng` | `en`   |      —      |           |    ✔       |            |
| Esperanto            | Esperanto     |`epo` | `eo`   |            |           |   ✔       |            |
| Spanish              | Español   |`spa` | `es`   |       ✔      |           |       ✔   |            |
| Estonian             | Eesti     |`est`    | `et`   |     ✔        |           |   ✔       |            |
| Basque               | Euskara   |`eus` | `eu`   |     ✔      |      ✔        |    ✔      |            |
| Persian              | فارسی          |`pes` | `fa`   |    —        |           |          |            |
| Finnish              | Suomi     |`fin` | `fi`   | ✔           |   ✔        |   ✔       |            |
| French               | Français     |`fra` | `fr`   |     —       |           |     ✔     |            |
| Frisian              | Frysk     |`fry` | `fy-NL`   |            |           |       ✔    |            |
| Irish                | Gaeilge     |`gle` | `ga-IE`   |            |           |    ✔      |            |
| Hindi                | हिन्दी      |`hin` | `hi`   |            |           |          |            |
| Upper Sorbian        | Hornjoserbšćina     |`hsb` | `hsb`   |            |           |       ✔   |            |
| Hungarian            | Magyar nyelv     |`hun` | `hu`   |      ✔       |           |     ✔     |            |
| Armenian             | Հայերեն         | `hye` | `hy-AM` | ✔        |          |       ✔   |             |
| Interlingua          | Interlingua     |`ina` | `ia`   |    ✔         |           |     ✔     |            |
| Indonesian           | Bahasa indonesia     |`ind` | `id`   |       ✔        |           |     ✔     |            |
| Italian              | Italiano     |`ita` | `it`   |     ✔       |           |    ✔      |            |
| Japanese             | 日本語     |`jpn` | `ja`   |      —      |           |     —     |            |
| Georgian             |  ქართული ენა    |`kat` | `ka`   |    ✔          |           | ✔         |            |
| Kabyle               | Taqbaylit     |`kab` | `kab`   |      ✔        |           |      ✔      |            |
| Kazakh               | Қазақша     |`kaz` | `kk`   |   ✔          |           |      ✔     |            |
| Kyrgyz               | Кыргызча     |`kir` | `ky`   |    ✔         |           |  ✔        |            |
| Komi-Zyrian          | Коми кыв     |`kpv` | `kv`   |       ✔       |           |  ✔        |            |
| Luganda              | Luganda     |`lug` | `lg`   |       ✔       |           |       ✔       |            |
| Lithuanian           | Lietuvių kalba     |`lit` | `lt`   |   ✔         |           |  ✔          |            |
| Latvian              | Latviešu valoda    |`lvs` | `lv`   |  ✔          |           |     ✔       |            |
| Mongolian            | Монгол хэл |`khk` | `mn`   | ✔          |        |    ✔   |           |
| Maltese              | Malti     |`mlt` | `mt`   |      ✔       |           |      ✔      |            |
| Dutch                | Nederlands     |`nld` | `nl`   |   ✔         |           |    ✔      |            |
| Oriya                | ଓଡ଼ିଆ     |`ori` | `or`   |            |           |          |            |
| Punjabi              | ਪੰਜਾਬੀ     |`pan` | `pa-IN`   |            |           |          |            |
| Polish               | Polski     |`pol` | `pl`   |   ✔          |           |     ✔     |            |
| Portuguese           | Português     |`por` | `pt`   |            |           |     ✔     |            |
| Kʼicheʼ              | Kʼicheʼ             |`quc` | `quc`   |   ✔          |           |      ✔    |            |
| Romansch (Sursilvan) | Romontsch     |`roh` | `rm-sursilv`   |            |           |  ✔        |            |
| Romansch (Vallader)  | Rumantsch     |`roh` | `rm-vallader`   |            |           |   ✔       |            |
| Romanian             | Românește     |`ron` | `ro`   |   ✔          |           |    ✔       |            |
| Russian              | Русский     |`rus` | `ru`   |            |           |     ✔     |            |
| Kinyarwanda          | Kinyarwanda     |`kin` | `rw`   |    ✔         |           |    ✔       |            |
| Sakha                | Саха тыла  |`sah` | `sah`   | ✔          |        |  ✔     |         |
| Slovenian            | Slovenščina     |`slv` | `sl`   | ✔           |           |    ✔      |            |
| Swedish              | Svenska      |`swe` | `sv-SE`   |     ✔        |           |     ✔     |            |
| Tamil                | தமிழ்    |`tam` | `ta`   |       ✔      |           |        ✔   |            |
| Thai                 | ภาษาไทย     |`tha` | `th`   |    ✔        |           |     ✔     |            |
| Turkish              | Türkçe |`tur` | `tr`   |   ✔         |           |      ✔     |            |
| Tatar                | Татар теле |`tat` | `tt`   | ✔          |        |  ✔     |         |
| Ukrainian            |  Українська мова    |`ukr` | `uk`   |   ✔         |           |    ✔       |            |
| Vietnamese           | Tiếng Việt     |`vie` | `vi`   |       ✔      |           |    ✔      |            |
| Votic                | Vaďďa tšeeli    |`vot` | `vot`   |            |           |   ✔       |            |
| Chinese (China)      | 中文     |`cmn` | `zh-CN`   |      —      |           |    —      |            |
| Chinese (Hong Kong)  | 中文     |`cmn` | `zh-HK`   |      —      |           |    —      |            |
| Chinese (Taiwan)     | 中文     |`cmn` | `zh-TW`   |      —      |           |    —      |            |

## How to use it

### Alphabet

```python
>>> from cvutils import Alphabet
>>> a = Alphabet('cv')
>>> a.get_alphabet()
' -абвгдежзийклмнопрстуфхцчшщыэюяёҫӑӗӳ'
```

### Grapheme to phoneme

```python
>>> from cvutils import Phonemiser
>>> p = Phonemiser('ab')
>>> p.phonemise('гӏапынхъамыз')
'ʕapənqaməz'

>>> p = Phonemiser('br')
>>> p.phonemise("implijout")
'impliʒut'
```

### Validator

```python
>>> from cvutils import Validator
>>> v = Validator('ab')
>>> v.validate('Аллаҳ хаҵеи-ԥҳәыси иеилыхны, аҭыԥҳацәа роума иалихыз?')
'аллаҳ хаҵеи-ԥҳәыси иеилыхны аҭыԥҳацәа роума иалихыз'

>>> v = Validator('br')
>>> v.validate('Ha cʼhoant hocʼh eus da gendercʼhel da implijout ar servijer-mañ ?')
"ha c'hoant hoc'h eus da genderc'hel da implijout ar servijer-mañ"
```

### Sentence segmentation

```python
>>> from cvutils import Segmenter 
>>> s = Segmenter('br')
>>> para = "Peurliesañ avat e kemm ar vogalennoù e c'hengerioù evit dont da vezañ heñvel ouzh ar vogalennoù en nominativ (d.l.e. ar stumm-meneg), da skouer e hungareg: Aour, tungsten, zink, uraniom, h.a., a vez kavet e kondon Bouryatia. A-bouez-bras evit armerzh ar vro eo al labour-douar ivez pa vez gounezet gwinizh ha legumaj dreist-holl. A-hend-all e vez gounezet arc'hant dre chaseal ha pesketa."
>>> for sent in s.segment(para):
...     print(sent)
... 
Peurliesañ avat e kemm ar vogalennoù e c'hengerioù evit dont da vezañ heñvel ouzh ar vogalennoù en nominativ (d.l.e. ar stumm-meneg), da skouer e hungareg: Aour, tungsten, zink, uraniom, h.a., a vez kavet e kondon Bouryatia.
A-bouez-bras evit armerzh ar vro eo al labour-douar ivez pa vez gounezet gwinizh ha legumaj dreist-holl.
A-hend-all e vez gounezet arc'hant dre chaseal ha pesketa.
```


## Frequently asked questions

### Why not use [insert better system] for [insert task here] ?

There are potentially lot of better language-specific systems for doing these tasks, but each one has
a slightly different API, so if you want to support all the Common Voice languages or even a reasonable
subset you have to learn and use the same number of language-specific APIs. 

The idea of these utilities is to provide adequate implementations of things are are likely to be useful
when working with all the languages in Common Voice. If you are working on a single language or have 
a specific setup or are using more data than just Common Voice, maybe this isn't for you. But if you
want to just train [coqui-ai/STT](https://github.com/coqui-ai/STT/) on Common Voice, then maybe it is :)

### Why not just make the alphabet from the transcripts ?

Depending on the language in Common Voice, the transcripts can contain a lot of random punctuation,
numerals, and incorrect character encodings (for example Latin *ç* instead of Cyrillic *ҫ* for Chuvash). These
may look the same but will result in bigger sparsity for the model. Additionally some languages may
have several encodings of the same character, such as the apostrophe. These will ideally be normalised
before training.

Also, if you are working with a single language you probably have time to look through all the transcripts
for the alphabetic symbols, but if you want to work with a large number of Common Voice languages at the 
same time it's useful to have them all in one place.

## See also

* [`epitran`](https://github.com/dmort27/epitran/): Great grapheme to phoneme system that supports a wide
  range of languages.

## Acknowledgements 

* Grapheme to phoneme correspondences for the following languages from [`epitran`](https://github.com/dmort27/epitran/):
  * `vi`, `uk`, `kk`, `ky`, `ta`
* Code for [transducer lookup](https://github.com/mhulden/foma/blob/master/foma/python/attapply.py) from Måns Huldén.

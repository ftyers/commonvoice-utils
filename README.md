# Common Voice Utils 

This repository collects together basic linguistic processing data for using dataset
dumps from the Common Voice project. It aims to provide a one-stop-shop for 
utilities and data useful in training ASR and TTS systems.

## Tools

* Phonemiser: A rudimentary grapheme to phoneme (g2p) system based on a deterministic longest-match left-to-right replacements of orthographic units
* Validator: A validation script that can be used with `import_cv2.py` from [coqui-ai/STT](https://github.com/coqui-ai/STT/)
* Alphabet: The relevant alphabet of the language, appropriate for use in training ASR
* Segmenter: A deterministic sentence segmentation algorithm tuned for segmenting paragraphs from Wikipedia

## Language support 

| Language | Autonym   | Code | Code (CV) | Phon | Valid | Alphabet | Segment |
|--------------------- |---------- |----- |------- |----------- |----------|---------- |------------|
| Abaza                | Абаза     |`abq` | `ab`   | ✔          | ✔         | ✔        |           |
| Arabic               | اَلْعَرَبِيَّةُ     |`ara` | `ar`   |            |           |          |            |
| Assamese             |  অসমীয়া    |`asm` | `as`   |            |           |          |            |
| Breton               | Brezhoneg |`bre` | `br`   | ✔          | ✔         | ✔        |      ✔     |
| Catalan              | Català     |`cat` | `ca`   |            |           |          |            |
| Czech                | Čeština     |`ces` | `cs`   |    ✔        |    ✔        |  ✔        |            |
| Hakha Chin           | Hakha Lai |`cnh` | `cnh`   |            |           |          |            |
| Chuvash              | Чӑвашла |`chv` | `cv`   | ✔          | ✔         | ✔        |      ✔     |
| Welsh                | Cymraeg     |`cym` | `cy`   |            |           |          |            |
| Dhivehi              | ދިވެހި |`div` | `dv`   | ✔          |        |      |         |
| Greek                | Ελληνικά |`ell` | `el`   | ✔          |        |      |         |
| German               | Deutsch     |`deu` | `de`   |            |           |          |            |
| English              | English     |`eng` | `en`   |            |           |          |            |
| Esperanto            | Esperanto     |`epo` | `eo`   |            |           |          |            |
| Spanish              | Español   |`spa` | `es`   |            |           |          |            |
| Estonian             | Eesti     |`est`    | `et`   |            |           |   ✔       |            |
| Basque               | Euskara   |`eus` | `eu`   |            |           |    ✔      |            |
| Persian              | فارسی          |`pes` | `fa`   |            |           |          |            |
| Finnish              | Suomi     |`fin` | `fi`   | ✔           |   ✔        |   ✔       |            |
| French               | Français     |`fra` | `fr`   |            |           |          |            |
| Frisian              | Frysk     |`fry` | `fy-NL`   |            |           |          |            |
| Irish                | Gaeilge     |`gle` | `ga-IE`   |            |           |    ✔      |            |
| Hindi                | हिन्दी      |`hin` | `hi`   |            |           |          |            |
| Upper Sorbian        | Hornjoserbšćina     |`hsb` | `hsb`   |            |           |       ✔   |            |
| Hungarian            | Magyar nyelv     |`hun` | `hu`   |            |           |     ✔     |            |
| Interlingua          | Interlingua     |`ina` | `ia`   |            |           |          |            |
| Indonesian           | Bahasa indonesia     |`ind` | `id`   |            |           |     ✔     |            |
| Italian              | Italiano     |`ita` | `it`   |            |           |          |            |
| Japanese             | 日本語     |`jpn` | `ja`   |            |           |          |            |
| Georgian             |  ქართული ენა    |`kat` | `ka`   |    ✔          |           | ✔         |            |
| Kabyle               | Taqbaylit     |`kab` | `kab`   |            |           |          |            |
| Kazakh               | Қазақша     |`kaz` | `kk`   |   ✔          |           |          |            |
| Kyrgyz               | Кыргызча     |`kir` | `ky`   |    ✔         |           |  ✔        |            |
| Luganda              | Luganda     |`lug` | `lg`   |            |           |          |            |
| Lithuanian           | Lietuvių kalba     |`lit` | `lt`   |            |           |          |            |
| Latvian              | Latviešu valoda    |`lvs` | `lv`   |            |           |          |            |
| Mongolian            | Монгол хэл |`khk` | `mn`   | ✔          |        |      |         |
| Maltese              | Malti     |`mlt` | `mt`   |            |           |          |            |
| Dutch                | Nederlands     |`nld` | `nl`   |            |           |          |            |
| Oriya                | ଓଡ଼ିଆ     |`ori` | `or`   |            |           |          |            |
| Punjabi              | ਪੰਜਾਬੀ     |`pan` | `pa-IN`   |            |           |          |            |
| Polish               | Polski     |`pol` | `pl`   |            |           |     ✔     |            |
| Portuguese           | Português     |`por` | `pt`   |            |           |     ✔     |            |
| Romansch (Sursilvan) | Romontsch     |`roh` | `rm-sursilv`   |            |           |  ✔        |            |
| Romansch (Vallader)  | Rumantsch     |`roh` | `rm-vallader`   |            |           |   ✔       |            |
| Romanian             | Românește     |`ron` | `ro`   |            |           |          |  ✔          |
| Russian              | Русский     |`rus` | `ru`   |            |           |     ✔     |            |
| Kinyarwanda          | Kinyarwanda     |`kin` | `rw`   |            |           |          |            |
| Sakha                | Саха тыла  |`sah` | `sah`   | ✔          |        |      |         |
| Slovenian            | Slovenščina     |`slv` | `sl`   |            |           |    ✔      |            |
| Swedish              | Svenska      |`swe` | `sv-SE`   |            |           |     ✔     |            |
| Tamil                | தமிழ்    |`tam` | `ta`   |            |           |          |            |
| Thai                 | ภาษาไทย     |`tha` | `th`   |    ✔        |           |     ✔     |            |
| Turkish              | Türkçe |`tur` | `tr`   |   ✔         |           |          |            |
| Tatar                | Татар теле |`tat` | `tt`   | ✔          |        |  ✔     |         |
| Ukrainian            |  Українська мова    |`ukr` | `uk`   |   ✔         |           |          |            |
| Vietnamese           | Tiếng Việt     |`vie` | `vi`   |            |           |          |            |
| Votic                | Vaďďa tšeeli    |`vot` | `vot`   |            |           |          |            |
| Chinese (China)      | 中文     |`cmn` | `zh-CN`   |            |           |          |            |
| Chinese (Hong Kong)  | 中文     |`cmn` | `zh-HK`   |            |           |          |            |
| Chinese (Taiwan)     | 中文     |`cmn` | `zh-TW`   |            |           |          |            |

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


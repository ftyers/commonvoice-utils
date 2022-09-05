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
  * A validation and normalisation script.
  * It checks a sentence to see if it can be converted and if possible normalises the encoding, removes punctuation and returns it
* Alphabet: 
  * The relevant alphabet of the language, appropriate for use in training ASR
* Segmenter: 
  * A deterministic sentence segmentation algorithm tuned for segmenting paragraphs from Wikipedia
* Corpora:
  * Contains metadata for different corpora you may be interested in using with Common Voice

## Installation

The easiest way is with `pip`:

```bash
$ pip install git+https://github.com/ftyers/commonvoice-utils.git
```

## How to use it

### Command line tool

There is also a command line tool, `covo` /ˈkəʊvəʊ/ which aims to expose much of the functionality
through the command line. Some examples on the next lines:

#### Process a Wikipedia dump

Use a Wikipedia dump to get text for a language mode in the right format:

```bash
$ covo dump mtwiki-latest-pages-articles.xml.bz2 | covo segment mt | covo norm mt
x'inhi l-wikipedija
il-wikipedija hi mmexxija mill-fondazzjoni wikimedia fondazzjoni mingħajr fini ta' lukru li tospita proġetti oħra b'kontenut ħieles u multilingwi
il-malti huwa l-ilsien nazzjonali tar-repubblika ta' malta
huwa l-ilsien uffiċjali flimkien mal-ingliż kif ukoll wieħed mill-ilsna uffiċjali tal-unjoni ewropea
```

#### Query the OPUS corpus collection

Get a list of URLs for a particular language from the OPUS corpus collection:

```bash
$ covo opus mt | sort -gr
23859 documents,69.4M tokens	https://object.pouta.csc.fi/OPUS-DGT/v2019/mono/mt.txt.gz
8665 documents,25.8M tokens	https://object.pouta.csc.fi/OPUS-JRC-Acquis/v3.0/mono/mt.txt.gz
5388 documents,8.9M tokens	https://object.pouta.csc.fi/OPUS-JW300/v1b/mono/mt.txt.gz
...
```

#### Convert grapheme input to phonemes

Get the grapheme to phoneme output for some arbitrary input:

```bash
$ echo "euskal herrian euskaraz" | covo phon eu
eus̺kal erian eus̺kaɾas̻

$ echo "قايتا نىشان بەلگىلەش ئورنى ئۇيغۇرچە ۋىكىپىدىيە" | covo phon ug
qɑjtɑ nɪʃɑn bɛlɡɪlɛʃ ornɪ ujʁurtʃɛ vɪkɪpɪdɪjɛ
```

#### Export data for use in Coqui STT

Designed for use with [Coqui STT](https://github.com/coqui-ai/STT/), converts 
to 16kHz mono-channel PCM .wav files and runs the transcripts through the validation
step. In addition outputs `.csv` files for each of the input `.tsv` files. The 
structure of the command is:

```bash
$ covo export coqui [language code] [common voice dataset directory]
```

For example for Erzya, `myv`:

```bash
$ covo export myv cv-corpus-8.0-2022-01-19/myv/
Loading TSV file:  cv-corpus-8.0-2022-01-19/myv/test.tsv
  Importing mp3 files...
  Imported 292 samples.
  Skipped 2 samples that were longer than 10 seconds.
  Final amount of imported audio: 0:27:03 from 0:27:23.
  Saving new Coqui STT-formatted CSV file to:  cv-corpus-8.0-2022-01-19/myv/clips/test.csv
  Writing CSV file for train.py as:  cv-corpus-8.0-2022-01-19/myv/clips/test.csv
```

#### Export data for use in NVIDIA NeMo

Designed for use with [NVIDIA's Nemo](https://github.com/NVIDIA/NeMo), converts 
to 16kHz mono-channel PCM .wav files and runs the transcripts through the validation
step. In addition outputs `.json` files for each of the input `.tsv` files. The 
structure of the command is:


```bash
$ covo export nemo [language code] [common voice dataset directory]
```

For example for Sardinian, `sc`:

```bash
INFO:root:Find existing folder /tmp/cv-corpus-10.0-2022-07-04/sc/
INFO:root:Converting mp3 to wav for /tmp/cv-corpus-10.0-2022-07-04/sc/test.tsv.
100%|█████████████████████████████████████| 98/98 [00:00<00:00, 466.73it/s]
INFO:root:Creating manifests...
100%|█████████████████████████████████████| 98/98 [00:00<00:00, 94059.91it/s]
INFO:root:Converting mp3 to wav for /tmp/cv-corpus-10.0-2022-07-04/sc/dev.tsv.
100%|█████████████████████████████████████| 79/79 [00:00<00:00, 494.77it/s]
INFO:root:Creating manifests...
100%|█████████████████████████████████████| 79/79 [00:00<00:00, 100744.91it/s]
INFO:root:Converting mp3 to wav for /tmp/cv-corpus-10.0-2022-07-04/sc/train.tsv.
100%|█████████████████████████████████████| 200/200 [00:00<00:00, 497.96it/s]
INFO:root:Creating manifests...
100%|█████████████████████████████████████| 200/200 [00:00<00:00, 113836.45it/s]
```

### Python module

The code can also be used as a Python module, here are some examples:

#### Alphabet

Returns an alphabet appropriate for end-to-end speech recognition.

```python
>>> from cvutils import Alphabet
>>> a = Alphabet('cv')
>>> a.get_alphabet()
' -абвгдежзийклмнопрстуфхцчшщыэюяёҫӑӗӳ'
```

#### Corpora

Some miscellaneous tools for working with corpora:

```python
>>> from cvutils import Corpora
>>> c = Corpora('kpv')
>>> c.dump_url()
'https://dumps.wikimedia.org/kvwiki/latest/kvwiki-latest-pages-articles.xml.bz2'
>>> c.target_segments()
[]
>>> c = Corpora('cv')
>>> c.target_segments()
['нуль', 'пӗрре', 'иккӗ', 'виҫҫӗ', 'тӑваттӑ', 'пиллӗк', 'улттӑ', 'ҫиччӗ', 'саккӑр', 'тӑххӑр', 'ҫапла', 'ҫук']
>>> c.dump_url()
'https://dumps.wikimedia.org/cvwiki/latest/cvwiki-latest-pages-articles.xml.bz2'
```

#### Grapheme to phoneme

For a given token, return an approximate broad phonemised version of it.

```python
>>> from cvutils import Phonemiser
>>> p = Phonemiser('ab')
>>> p.phonemise('гӏапынхъамыз')
'ʕapənqaməz'

>>> p = Phonemiser('br')
>>> p.phonemise("implijout")
'impliʒut'
```

#### Validator

For a given input sentence/utterance, the validator returns either a validated and normalised
version of the string according to the validation rules, or `None` if the string cannot be 
validated.

```python
>>> from cvutils import Validator
>>> v = Validator('ab')
>>> v.validate('Аллаҳ хаҵеи-ԥҳәыси иеилыхны, аҭыԥҳацәа роума иалихыз?')
'аллаҳ хаҵеи-ԥҳәыси иеилыхны аҭыԥҳацәа роума иалихыз'

>>> v = Validator('br')
>>> v.validate('Ha cʼhoant hocʼh eus da gendercʼhel da implijout ar servijer-mañ ?')
"ha c'hoant hoc'h eus da genderc'hel da implijout ar servijer-mañ"
```

#### Sentence segmentation

Mostly designed for use with Wikipedia, takes a paragraph and returns a list of the 
sentences found within it.

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

## Language support 

| Language             | Autonym       | Code | (CV) | (WP) | Phon | Valid | Alphabet | Segment |
|--------------------- |-------------- |----- |------|----- |----------- |----------|---------- |------------|
| Abkhaz                | Аԥсуа         |`abk` | `ab` |  —  | ✔          | ✔         | ✔        |           |
| Amharic              | አማርኛ          | `amh` | —  | `am` | ✔           |      ✔      | ✔         |           |
| Arabic               | اَلْعَرَبِيَّةُ       |`ara` | `ar` | `ar`  |     —       |   ✔         |          ✔  |            |
| Assamese             |  অসমীয়া    |`asm` | `as`   |   `as` |   ✔      |       ✔   |    ✔     |            |
| Asturian             | Asturianu | `ast` | `ast` | `ast` |         |  ✔         |  ✔       |          | 
| Azeri                | Azərbaycanca | `aze` | `az` | `az` |         |  ✔         |  ✔       |          | 
| Bashkort             | Башҡортса     |`bak` | `ba`  |  `ba` |     ✔      |   ✔       | ✔        |           |
| Basaa                | Basaa         |`bas` | `bas`  |  — |     ✔      |      ✔      | ✔        |           |
| Belarusian           | Беларуская мова |`bel` | `be`  |  `be` |     ✔      |   ✔         | ✔        |           |
| Bengali              | বাংলা            |`ben` | `bn`  |  `bn` |          |   ✔       | ✔        |   ✔        |
| Breton               | Brezhoneg     |`bre` | `br`   | `br` | ✔          | ✔         | ✔        |      ✔     |
| Bulgarian            | Български | `bul` | `bg`   | `bg` | ✔          |    ✔      | ✔        |           |
| Catalan              | Català        |`cat` | `ca`   | `ca` |            |    ✔        |      ✔    |            |
| Czech                | Čeština       |`ces` | `cs`   |`cs` |    ✔        |    ✔        |  ✔        |            |
| Chukchi              | Ԓыгъоравэтԓьэн |`ckt` | —   | — | ✔          | ✔         | ✔        |           |
| Chuvash              | Чӑвашла       |`chv` | `cv`   |`cv`| ✔          | ✔         | ✔        |      ✔     |
| Hakha Chin           | Hakha Lai     |`cnh` | `cnh`  |—  |            |      ✔      |     ✔      |            |
| Highland Chatino     |  —            |`ctp` |  —   |  — |             |        ✔     |     ✔      |            |
| Welsh                | Cymraeg       |`cym` | `cy`   |`cy`|       ✔      |        ✔     |     ✔      |            |
| Dhivehi              | ދިވެހި           |`div` | `dv`   |`dv`| ✔          |    ✔     |   ✔    |      ✔    |
| Greek                | Ελληνικά      |`ell` | `el`   |`el`| ✔          |      ✔   |  ✔      |         |
| Danish               | Dansk         |`dan` | `da`   |`da`|            |     ✔    |     ✔      |            |
| German               | Deutsch       |`deu` | `de`   |`de`|            |          ✔  |     ✔      |            |
| English              | English       |`eng` | `en`   |`en`|      —      |    ✔        |    ✔       |            |
| Esperanto            | Esperanto     |`epo` | `eo`   |`eo`|            |      ✔      |   ✔       |            |
| Ewe                  | Eʋegbe        |`ewe` | `ee`   |`ee`|      ✔        |      ✔      |   ✔       |            |
| Spanish              | Español             |`spa` | `es`   |`es`|       ✔      |    ✔        |       ✔   |            |
| Erzya                | Эрзянь кель |`myv`    | `myv`   |`myv`|             |    ✔         |   ✔       |            |
| Estonian             | Eesti               |`est`    | `et`   |`et`|     ✔        |    ✔         |   ✔       |            |
| Basque               | Euskara             |`eus` | `eu`   |`eu`|     ✔      |      ✔        |    ✔      |     ✔        |
| Persian              | فارسی               |`pes` | `fa`   |`fa`|    —        |       ✔    |    ✔      |            |
| Finnish              | Suomi               |`fin` | `fi`   |`fi`| ✔           |   ✔        |   ✔       |            |
| French               | Français            |`fra` | `fr`   |`fr`|     —       |        ✔     |     ✔     |            |
| Frisian              | Frysk               |`fry` | `fy-NL`   |`fy`|            |     ✔       |       ✔    |     ✔        |
| Igbo                 | Ásụ̀sụ́ Ìgbò          |`ibo` | `ig`   |`ig`|    ✔        |       ✔      |    ✔      |            |
| Irish                | Gaeilge             |`gle` | `ga-IE`   |`ga`|            |    ✔       |    ✔      |            |
| Galician             | Galego              |`glg` | `gl`   |`gl`|       ✔       |    ✔       |    ✔      |            |
| Guaraní              | Avañeʼẽ             |`gug` | `gn`   |`gn`|       ✔       |    ✔      |    ✔      |            |
| Hindi                | हिन्दी                                              |`hin` | `hi`   | `hi`           |       ✔    |      ✔    |       ✔     |
| Hausa                | Harshen Hausa       |`hau` | `ha`  |`ha` |     ✔       |    ✔        |       ✔   |             |
| Upper Sorbian        | Hornjoserbšćina     |`hsb` | `hsb`  |`hsb` |            |       ✔     |       ✔   |       ✔      |
| Hungarian            | Magyar nyelv     |`hun` | `hu`  |`hu` |      ✔       |       ✔       |     ✔     |            |
| Armenian             | Հայերեն         | `hye` | `hy-AM` |`hy`| ✔        |      ✔     |       ✔   |             |
| Interlingua          | Interlingua     |`ina` | `ia`  |`ia` |    ✔         |    ✔        |     ✔     |            |
| Indonesian           | Bahasa indonesia     |`ind` | `id` |`id`  |       ✔        |       ✔     |     ✔     |            |
| Icelandic            | Íslenska |`isl` | `is` |`is`  |            |       ✔     |    ✔      |            |
| Italian              | Italiano     |`ita` | `it` |`it`  |     ✔       |  ✔         |    ✔      |            |
| Japanese             | 日本語     |`jpn` | `ja`   |`ja`|      —      |           |     —     |            |
| Georgian             |  ქართული ენა    |`kat` | `ka`  |`ka` |    ✔          |      ✔      | ✔         |            |
| Kabyle               | Taqbaylit     |`kab` | `kab`  |`kab` |      ✔        |     ✔       |      ✔      |            |
| Kazakh               | Қазақша     |`kaz` | `kk`  |`kk` |   ✔          |     ✔        |      ✔     |            |
| Kikuyu               | Gĩgĩkũyũ    | `kik` | `ki` | `ki` |  ✔          |     ✔        |      ✔     |            |
| Kyrgyz               | Кыргызча     |`kir` | `ky`  |`ky` |    ✔         |     ✔        |  ✔        |    ✔          |
| Kurmanji Kurdish     | Kurmancî    |`kmr` | `ku`  |`ku` |      ✔       |   ✔          |   ✔       |              |
| Sorani Kurdish       | سۆرانی  |`ckb` | `ckb`  |`ckb` |      ✔       |   ✔          |   ✔       |              |
| Komi-Zyrian          | Коми кыв     |`kpv` | `kv`  |`kv` |       ✔       |           |  ✔        |            |
| Luganda              | Luganda     |`lug` | `lg`  |`lg` |       ✔       |        ✔     |       ✔       |            |
| Lithuanian           | Lietuvių kalba     |`lit` | `lt` |`lt`  |   ✔         |      ✔      |  ✔          |            |
| Lingala              | Lingála     |`lin` | `ln` |`ln`  |            |      ✔      |  ✔          |            |
| Latvian              | Latviešu valoda    |`lvs` | `lv` |`lv`  |  ✔          |      ✔     |     ✔       |            |
| Luo                  | Dholuo             |`luo` | `luo` | —  |  ✔          |      ✔     |     ✔       |            |
| Macedonian           | Македонски |`mkd` | `mk`  |`mk` |           |   ✔    |    ✔   |             |
| Malayalam            | മലയാളം  |`mal` | `ml`  |`ml` |           |    ✔      |    ✔   |            |
| Marathi              | मराठी           |`mar` | `mr`  |`mr` |           |    ✔   |    ✔   |             |
| Hill Mari            | Мары йӹлмӹ |`mrj` | `mrj`  |`mrj` |           |   ✔     |    ✔   |             |
| Meadow Mari          | Олык марий |`mhr` | `mhr`  |`mhr` |           |   ✔     |    ✔   |             |
| Mongolian            | Монгол хэл |`khk` | `mn`  |`mn` | ✔          |   ✔     |    ✔   |        ✔     |
| Moksha               | Мокшень кяль |`mdf` | `mdf`  |`mdf` | ✔          |   ✔      |     ✔     |  |
| Maltese              | Malti     |`mlt` | `mt`  |`mt` |      ✔       |      ✔     |      ✔      |         ✔   |
| Yoloxóchitl Mixtec   |           | `xty` | — | —  |                  |   ✔     |      ✔      |                |
| Dutch                | Nederlands     |`nld` | `nl` |`nl`  |   ✔         |     ✔      |    ✔      |            |
| Chewa                | Chichewa       | `nya` | `ny` | `ny` |   ✔         |     ✔      |    ✔      |            |
| Sierra Puebla Nahuatl | —  | `azz` |— | — |   ✔      |  ✔         |  ✔       |          | 
| Nepali               |  नेपाली|`ne` | `ne`  |`ne` |             |      ✔     |      ✔      |            |
| Norwegian Nynorsk    | Nynorsk |`nno` | `nn-NO` |`nn`  |            |     ✔      |    ✔      |            |
| Oriya                | ଓଡ଼ିଆ                                       |`ori` | `or`  |`or` |            |     ✔      |    ✔      |        ✔     |
| Punjabi              | ਪੰਜਾਬੀ     |`pan` | `pa-IN`   | `pa`  |          |       ✔    |     ✔     |            |
| Polish               | Polski     |`pol` | `pl`  |`pl` |   ✔          |       ✔     |     ✔     |            |
| Portuguese           | Português     |`por` | `pt`  |`pt` |            |    ✔        |     ✔     |            |
| Kʼicheʼ              | Kʼicheʼ             |`quc` | — | — |   ✔          |   ✔        |      ✔    |            |
| Romansch (Sursilvan) | Romontsch     |`roh` | `rm-sursilv`  |`rm` |            |      ✔     |  ✔        |        ✔      |
| Romansch (Vallader)  | Rumantsch     |`roh` | `rm-vallader`  |`rm` |            |     ✔      |   ✔       |        ✔      |
| Romanian             | Românește     |`ron` | `ro`  |`ro` |   ✔          |    ✔         |    ✔       |            |
| Russian              | Русский     |`rus` | `ru`   |`ru`|            |      ✔      |     ✔     |            |
| Kinyarwanda          | Kinyarwanda     |`kin` | `rw` |`rw`  |    ✔         |     ✔       |    ✔       |            |
| Sakha                | Саха тыла  |`sah` | `sah`   |`sah`| ✔          |      ✔  |  ✔     |      ✔    |
| Sardinian            | Limba sarda |`srd` | `sc`   |`sc`|           |      ✔  |  ✔     |          |
| Santali              | ᱥᱟᱱᱛᱟᱲᱤ |`sat` | `sat`   |`sat`| ✔          |      ✔  |  ✔     |          |
| Saraiki              | |`skr` | `skr`   | — | ✔          |      ✔  |  ✔     |          |
| Serbian              | Srpski  |`srp` | `sr`  |`sr` | ✔           |     ✔      |    ✔      |            |
| Slovak               | Slovenčina |`slk` | `sk`  |`sk` | ✔           |   ✔         |    ✔      |            |
| Slovenian            | Slovenščina     |`slv` | `sl`  |`sl` | ✔           |   ✔         |    ✔      |            |
| Swahili              | Kiswahili    |`swa` | —  |`sw` |     ✔        |     ✔        |     ✔     |            |
| Swedish              | Svenska      |`swe` | `sv-SE`  |`sv` |     ✔        |     ✔        |     ✔     |            |
| Tamil                | தமிழ்    |`tam` | `ta`   |`ta`|       ✔      |     ✔      |        ✔   |            |
| Thai                 | ภาษาไทย     |`tha` | `th`  |`th` |    ✔        |    ✔       |     ✔     |            |
| Tigre                | ትግራይት |`tig` | `ti`  |`tig` |            |       ✔     |      ✔     |             |
| Tigrinya             | ትግርኛ |`ti` | `ti`  |`ti` |            |       ✔     |      ✔     |             |
| Turkish              | Türkçe |`tur` | `tr`  |`tr` |   ✔         |       ✔     |      ✔     |        ✔     |
| Tatar                | Татар теле |`tat` | `tt`  |`tt` | ✔          |   ✔     |  ✔     |     ✔      |
| Highland Totonac     | —          |`tos` | —  | — |           |   ✔     |  ✔     |           |
| Twi                  | Twi        | `tw` | `tw`  | `tw` | ✔          |   ✔     |  ✔    |            |
| Ukrainian            |  Українська мова    |`ukr` | `uk` |`uk`  |   ✔         |     ✔      |    ✔       |            |
| Urdu                 | اُردُو |`urd` | `ur` |`ur`  |   ✔         |      ✔      |    ✔       |            |
| Uyghur               | ئۇيغۇر تىلى |`uig` | `ug` |`ug`  |   ✔         |    ✔        |    ✔       |            |
| Uzbek                | Oʻzbekcha |`uzb` | `uz` |`uz`  |   ✔         |   ✔        |    ✔       |            |
| Vietnamese           | Tiếng Việt     |`vie` | `vi` |`vi`  |       ✔      |       ✔     |    ✔      |       ✔      |
| Votic                | Vaďďa tšeeli    |`vot` | `vot` |  —  |            |      ✔      |   ✔       |            |
| Wolof                | Wolof |`wol` | —  |  `wo`  |      ✔        |      ✔       |   ✔       |            |
| Yoruba               | Èdè Yorùbá  |`yor` | —  |  `yo`  |      ✔        |      ✔       |   ✔       |            |
| Chinese (China)      | 中文     |`cmn` | `zh-CN` |`zh`  |      —      |           |    —      |            |
| Chinese (Hong Kong)  | 中文     |`cmn` | `zh-HK`  |`zh` |      —      |           |    —      |            |
| Chinese (Taiwan)     | 中文     |`cmn` | `zh-TW`   |`zh`|      —      |           |    —      |            |


## Frequently asked questions

### Why not use [insert better system] for [insert task here] ?

There are potentially a lot of better language-specific systems for doing these tasks, but each one has
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

### Hey aren't some of those languages not in Common Voice ?

That's right, some of the languages are either not in Common Voice (yet!) or are in Common Voice but have
not been released yet. If I've been working with them I've included them anyway.

## See also

* [`epitran`](https://github.com/dmort27/epitran/): Great grapheme to phoneme system that supports a wide
  range of languages.

## Licence

All the code, aside from that explicitly licensed under a different licence, is licensed under 
the [AGPL v 3.0](https://www.gnu.org/licenses/agpl-3.0.en.html).

## Acknowledgements 

* Grapheme to phoneme correspondences for the following languages from [`epitran`](https://github.com/dmort27/epitran/):
  * `vi`, `uk`, `kk`, `ky`, `ta`
* Code for [transducer lookup](https://github.com/mhulden/foma/blob/master/foma/python/attapply.py) from Måns Huldén.
* Code for [Wikipedia extraction](https://github.com/apertium/WikiExtractor) from Apertium.
* Code for [Coqui export](https://github.com/coqui-ai/STT/blob/main/bin/import_cv2.py) from [Coqui](https://coqui.ai).
* Code for [NeMo export](https://github.com/NVIDIA/NeMo/blob/0e57b58a849f6275629910cdeebd608e528327bf/scripts/dataset_processing/get_commonvoice_data.py) from [NVIDIA](http://www.nvidia.com)

# Common Voice Utils 

This repository collects together linguistic processing data for using dataset
dumps from the Common Voice project. It aims to provide a one-stop-shop for 
utilities and data useful in training ASR and TTS systems.

## Language support 

| Language | Autonym   | Code | CV Code | Phonemiser | Validator | Alphabet | Segmenter |
|--------- |---------- |----- |------- |----------- |----------|---------- |------------|
| Abaza    | Абаза     |`abq` | `ab`   | ✔          | ✔         | ✔        |           |
| Breton   | Brezhoneg |`bre` | `br`   | ✔          | ✔         | ✔        |           |



## How to use it

### Grapheme to phoneme

```python
>>> from phonemiser import Phonemiser
>>> p = Phonemiser('ab')
>>> p.phonemise('гӏапынхъамыз')
'ʕapənqaməz'

>>> p = Phonemiser('br')
>>> p.phonemise("implijout")
'impliʒut'
```

### Validator

```python
>>> from validator import Validator
>>> v = Validator('ab')
>>> v.validate('Аллаҳ хаҵеи-ԥҳәыси иеилыхны, аҭыԥҳацәа роума иалихыз?')
'аллаҳ хаҵеи-ԥҳәыси иеилыхны аҭыԥҳацәа роума иалихыз'

>>> v = Validator('br')
>>> v.validate('Ha cʼhoant hocʼh eus da gendercʼhel da implijout ar servijer-mañ ?')
"ha c'hoant hoc'h eus da genderc'hel da implijout ar servijer mañ"
```


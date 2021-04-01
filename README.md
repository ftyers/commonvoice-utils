# Common Voice Utils 

This repository collects together linguistic processing data for using dataset
dumps from the Common Voice project. It aims to provide a one-stop-shop for 
utilities and data useful in training ASR and TTS systems.

## Language support 

| Language | Code | CV Code | Phonemiser | Validator | Alphabet | Segmenter |
|--------- |----- |-------- |----------- |---------- |----------|---------- |
| Abaza    | `aba` | `ab`   | ✔          | ✔         | ✔        |           |


## How to use it

### Grapheme to phoneme

```python
>>> from phonemiser import Phonemiser
>>> p = Phonemiser('ab')
>>> p.phonemise('гӏапынхъамыз')
'ʕapənqaməz'
```

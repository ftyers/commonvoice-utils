# Troubleshooting

## Encoding issues

If you get something like: 

```python
 File "/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6/encodings/ascii.py", line 26, in decode
    return codecs.ascii_decode(input, self.errors)[0]
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 1: ordinal not in range(128)```
```

Look at your locale, you will need a UTF-8 compatible locale. You should check:

```bash
$ locale
```

and 

```python
import sys
sys.stdout.encoding
```


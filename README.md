# swsf scramble

This module implements the cheat code scrambling algorithm from Star Wars: Jedi Starfighter. It can be used to generate hashes for cheat codes, and search for cheat codes by hash.

## Usage

Install dependencies with `pip install -r requirements.txt`.

### Hashing

To generate a hash for a string, use the `swsf_scramble.py` script as follows:

```
python swsf_scramble.py <input string>
```

For example:

```
$ python swsf_scramble.py "DIRECTOR"
2C75827E
```

### Searching

To search for a cheat code by hash, use the `hash_search.py` script as follows:

```
python hash_search.py [-l MAX_LENGTH] [-d DICT_FILE] HASH1 [HASH2 ...]
```

### Dictionary search

If you pass a dictionary file to the search script, it will search for cheat codes that are valid words in the dictionary. The dictionary file should be a text file with one word per line.

Example:

```
$ python3 hash_search.py -l 8 -d /usr/share/dict/words 2C8574D8 2C78839F 2C75827E 6F4E45A6 4975AC40 49758D30 0EB12C00
Starting dictionary search using /usr/share/dict/words...
Found 6 matches in 0.23s.
Maggie (4975AC40)
NPR's (0EB12C00)
Quentin (6F4E45A6)
director (2C75827E)
now's (0EB12C00)
pew's (0EB12C00)1 matches in 0.26s.
director (2C75827E)
```

#### Brute force search

If you do not specify a dictionary file, the search script will perform a brute force search. This will take a long time depending on the length you specify. The results be written to a file called `matches.txt` in the current directory.

Example:

```
$ python3 hash_search.py -l 6 2C8574D8 2C78839F 2C75827E 6F4E45A6 4975AC40 49758D30 0EB12C00
Starting brute force search...
Searching for hashes ['2C8574D8', '2C78839F', '2C75827E', '6F4E45A6', '4975AC40', '49758D30', '0EB12C00'] of length 6 or less...
There are 308,915,776 possible words to check.
Progress: 0.02% (244 matches found, ~2029s remaining)
```

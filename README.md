# SWSF Scramble Scripts

This module comprises scripts for working with the cheat code scrambling algorithm from [Star Wars: Jedi Starfighter](https://en.wikipedia.org/wiki/Star_Wars:_Jedi_Starfighter). They can be used to generate code hashes and search for cheat codes by hash using brute force or a dictionary list.

## Setup

Install dependencies with `pip install -r requirements.txt`.

## Overview

The Star Wars: Jedi Starfighter cheat code screen has a text box that accepts any string from 1-8 characters. When the player enters a string, the game scrambles it using a simple algorithm and compares the result to a list of known cheat codes. If the scrambled string matches a cheat code, the cheat is activated.

The scrambling algorithm is as follows:
1. Convert the input string to lowercase.
2. Insert `code_` at the beginning of the string.
3. Set the hash value to 0x0.
3. For each character in the string:
    1. Convert the character to its ASCII value.
    2. Multiply the current hash value by 0x5.
    3. Add the ASCII value to the hash value.

Due to the way the algorithm works, there are many different strings that will produce the same hash (these are called [hash collisions](https://en.wikipedia.org/wiki/Hash_collision)). For example, the string `JARJAR` will produce the hash `2C75827E`, but so will `GOXBOW`, `JOISTY`, `LDONUT`, and countless others. This means that the game will accept any of those strings as a valid cheat codes.

## Hashing

To generate a hash for a string, use the `scramble.py` script as follows:

```bash
python scramble.py <input string>
```

For example:

```bash
$ python scramble.py DIRECTOR
2C75827E
```

## Searching

To search for a cheat code by hash, use the `search.py` script as follows:

```bash
python search.py [--max_length N] [--min-length N] [-d DICT_FILE] HASH1 [HASH2 ...]
```

### Dictionary search

If you pass a dictionary file to the search script, it will search for cheat codes that are valid words in the dictionary. The dictionary file should be a text file with one word per line. For example:
```bash
$ python search.py -d ../words.txt 2C8574D8 2C78839F 2C75827E 6F4E45A6 4975AC40 49758D30 0EB12C00
Starting dictionary search using ../words.txt...
Found 8 matches in 1.31s.
director (2C75827E)
furfur (49758D30)
headhunt (2C78839F)
Kirbie (4975AC40)
Maggie (4975AC40)
okehs (0EB12C00)
pew's (0EB12C00)
Quentin (6F4E45A6)
```

If you are on linux, a dictionary file can usually be found at `/usr/share/dict/words`.

### Brute force search

If you do not specify a dictionary file, the script will perform a brute force search. This can take a long time depending on the length you specify. The results be written to a file called `matches.txt` in the current directory. For example:

```bash
$ python search.py --min-length 4 --max-length 6 2C8574D8 2C78839F 2C75827E 6F4E45A6 4975AC40 49758D30 
0EB12C00
Starting brute force search...
Searching for codes matching ['2C8574D8', '2C78839F', '2C75827E', '6F4E45A6', '4975AC40', '49758D30', '0EB12C00'] between 4 and 6 letters...
There are 308,898,200 possible codes to check.
Progress: 0.84% (0 matches found, ~2986s remaining)
```

## Dictionary generation

If you want to generate a dictionary file for searching, use the `gen_dict.py` script as follows:

```bash
python gen_dict.py INPUT_FILE [-o OUTPUT_FILE] [-e ENCODING]
```

The input can be any text file, and the output will be a text file containing all the words from the input file on separate lines.

If the input encoding is not UTF-8 you must specify it. The output file encoding will always be UTF-8. Also, if you don't specify the output file name, it will be the input file name with `.dict` appended to the end.

For example:

```bash
# starwars.txt

A long time ago, in a galaxy far, far away
```

```bash
$ python gen_dict.py starwars.txt -o words.txt
```

```bash
# words.txt

A
long
time
ago
in
a
galaxy
far
far
away
```

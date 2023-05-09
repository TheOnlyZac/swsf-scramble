"""
swsf_scramble.py
author: theonlyzac
date: May 9 2023
version: 1.1

Hashes a string according to the cheat code scrambling algorithm in Star Wars Jedi Starfighter. Credit to modeco80 for reversing the hash function.

v1.1
Changed output of swsf_scramble from int to hex string.
Tweaked output of formatHex to remove the leading 0x.
"""
import sys

def swsf_scramble(code):
    """
    Returns the has for a given string.

    @param code the plaintext code to hash
    """
    code = 'code_' + code.lower()
    hash_result = 0
    for c in code:
        hash_result = (hash_result * 5) + ord(c)
    return formatHex(hash_result & 0xFFFFFFFF)

def formatHex(num):
    """
    Formats a hex string with leading zeroes.

    @param num the number to format
    """
    return str.format("{:08X}", num)

def main(argc, argv):
    """
    Calls the hashing function with the given code.
    """
    if argc == 1:
        print(f'Usage:\n\tpython {sys.argv[0]} PASSWORD')
        return
    
    print(swsf_scramble(argv[1]))

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
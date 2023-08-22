"""
scramble.py

This file contains the scrambling algorithm used by Star Wars: Jedi Starfighter.
"""
import sys

def swsf_scramble(code):
    """
    Returns the hash for a given string.

    @param code the plaintext code to hash
    """
    hash_result = 0x00013402 # Hash of 'code_'
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
        print(f'Usage:\n\tpython {sys.argv[0]} CODE')
        return

    print(swsf_scramble(argv[1]))

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)

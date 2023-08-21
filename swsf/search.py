"""
search.py

This file contains the code for searching for a password given a hash and a length
"""
import os
import sys
import time
import argparse
from scramble import swsf_scramble

DEBUG = False

#todo implement min length and writing to output file
def dictionary_search(dict_file: str, goal_hashes: list, max_length: int = 8, min_length: int = 1, outfile: str = 'matches.txt') -> int:
    """
    Searches for a password in a dictionary file.

    @param dict_file the dictionary file to search
    @param goal_hashes the list of hashes to search for
    @param max_length the max length of the passwords to check
    @param min_length the min length of the passwords to check
    @param outfile the file to write the results to
    """
    matches = []

    if not os.path.isfile(dict_file):
        print(f'Error: {dict_file} is not a file.')
        return matches

    with open(dict_file, 'r', encoding='utf-8') as f:
        for word in f:
            word = word.strip()
            word_length = len(word)

            if max_length != 0 and word_length > max_length:
                continue

            word_hash = swsf_scramble(word)
            #if DEBUG:
            #    print(f'Checking {word} ({word_hash})')

            if word_hash in goal_hashes:
                matches.append(f'{word} ({word_hash})')
                #if DEBUG:
                #    print(f'Match found: {word} ({word_hash})')

    return matches

def brute_force_search(goal_hashes: list, max_length: int = 8, min_length = 1, outfile: str = 'matches.txt') -> list:
    """
    Searches for a password by brute force.

    @param goal_hashes the list of hashes to search for
    @param max_length the max length of the passwords to check
    @param min_length the min length of the passwords to check
    @param outfile the file to write the results to
    """
    matches = []
    num_matches = 0

    if outfile is not None:
        with open(outfile, 'w+', encoding='utf-8') as f:
            f.write(f'---- Hash collisions for {goal_hashes} with length {max_length} or less ----\n')

    num_possible_words = 26**max_length - 26**(min_length-1)

    if(max_length == min_length:
        print(f'Searching for codes matching {goal_hashes} with {max_length} letters...')
    else:
        print(f'Searching for codes matching {goal_hashes} between {min_length} and {max_length} letters...')
    print(f'There are {num_possible_words:,} possible codes to check.')

    start = time.time()
    now = start
    num_words_checked = 0

    for length in range(min_length, max_length + 1):
        for i in range(0, num_possible_words):
            # Estimate time remaining every 100k words
            if num_words_checked > 0 and num_words_checked % 100000 == 0:
                percent_done = num_words_checked / num_possible_words

                now = time.time()
                wps = num_words_checked / (now - start)
                words_remaining = num_possible_words - num_words_checked
                time_remaining = words_remaining / wps

                print(f'Progress: {percent_done * 100:.2f}% ({num_matches} matches found, ~{time_remaining:.0f}s remaining)', end='\r')

            # Generate word
            word = ''
            for j in range(0, length):
                word += chr(ord('a') + (i // (26**j)) % 26)

            # Scramble the word
            word_hash = swsf_scramble(word)
            if DEBUG:
                print(f'Checking {word} ({word_hash})')

            # Check the word against the goal hashes
            num_words_checked += 1
            if word_hash in goal_hashes:
                matches.append(f'{word} ({word_hash})')
                num_matches += 1

                if outfile is not None:
                    with open(outfile, 'a+', encoding='utf-8') as f:
                        f.write(f'{word} ({word_hash})\n')

                if DEBUG:
                    print(f'Match found: {word} ({word_hash})')

    print(f'Results have been written to {outfile}.')
    return matches

def main(argc, argv):
    """
    Main function, called when the program is run.
    """
    if argc == 1:
        print(f'Usage:\n\tpython {sys.argv[0]} [--max-length N] [--min-length N] [-d DICT_FILE] HASH1 [HASH2 ...] [-o OUTFILE]')
        print('If a dictionary file is not specified, it will brute force search all possible hashes.')
        return

    # Setup arguments
    parser = argparse.ArgumentParser(description='Brute force searches for a password given a hash and a length.')
    parser.add_argument('hashes', metavar='HASH', type=str, nargs='+', help='the hash to search for')
    parser.add_argument('--max-length', metavar='MAX_LENGTH', type=int, default=8, help='the max length of the code')
    parser.add_argument('--min-length', metavar='MIN_LENGTH', type=int, default=0, help='the min length of the code')
    parser.add_argument('-d', '--dict', metavar='DICT_FILE', type=str, help='the dictionary file to search')
    parser.add_argument('-o', '--outfile', metavar='OUTFILE', type=str, default='matches.txt', help='the file to write the results to')
    args = parser.parse_args()

    goal_hashes = args.hashes
    max_length = args.max_length
    min_length = args.min_length
    dict_file = args.dict
    outfile = args.outfile

    if max_length > min_length:
        print('Error: max length must be greater than or equal to min length.')
        return
    elif max_length < 0 or min_length < 0:
        print('Error: max length and min length must be greater than or equal to 0.')
        return
    elif max_length > 8 or min_length > 8:
        print('Warning: codes greater than 8 characters cannot be used in-game.')

    matches = []

    start = time.time()
    if dict_file is None:
        print("Starting brute force search...")
        matches = brute_force_search(goal_hashes, max_length, min_length, outfile)
    else:
        print(f"Starting dictionary search using {dict_file}...")
        matches = dictionary_search(dict_file, goal_hashes, max_length, min_length, outfile)

    end = time.time()
    print(f'Found {len(matches)} matches in {(end - start):.2f}s.')
    print('\n'.join(matches))

if __name__ == "__main__":
    main(len(sys.argv), sys.argv)

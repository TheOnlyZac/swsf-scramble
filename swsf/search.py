"""
search.py

This file contains the code for searching for a password given a hash and a length
"""
import os
import time
import argparse
from scramble import swsf_scramble

DEBUG = False

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

            if min_length != 0 and word_length < min_length:
                continue

            word_hash = swsf_scramble(word)

            if word_hash in goal_hashes:
                matches.append(f'{word} ({word_hash})')

    with open(outfile, 'w+', encoding='utf-8') as f:
        f.write(f'---- Hash collisions for {goal_hashes} of length {min_length}-{max_length} ----\n')
        f.write('\n'.join(matches))

    return matches

def brute_force_search(goal_hashes: list, max_length: int = 8, min_length = 1, prefix = None, outfile: str = 'matches.txt') -> list:
    """
    Searches for a password by brute force.

    @param goal_hashes the list of hashes to search for
    @param max_length the max length of the passwords to check
    @param min_length the min length of the passwords to check
    @param outfile the file to write the results to
    """
    matches = []
    num_matches = 0

    # Make sure max and min lengths are valid
    if max_length < min_length:
        print('Error: max length must be greater than or equal to min length.')
        return
    elif max_length < 0 or min_length < 0:
        print('Error: max length and min length must be greater than or equal to 0.')
        return
    elif max_length > 8 or min_length > 8:
        print('Warning: codes greater than 8 characters cannot be used in-game.')

    # Open the output file
    if outfile is not None:
        with open(outfile, 'w+', encoding='utf-8') as f:
            f.write(f'---- Hash collisions for {goal_hashes} of length {min_length}-{max_length} ----\n')

    # Make sure prefix is valid
    if prefix is None:
        prefix = ''

    prefix_len = len(prefix)
    if prefix_len > max_length:
        print('Error: prefix is longer than max length.')
        return matches

    # Calculate the number of possible words
    num_possible_words = 0
    for i in range(min_length - prefix_len, max_length - prefix_len + 1):
        num_possible_words += 26**i

    # Print some info
    if max_length == min_length:
        print(f'Searching for codes matching {goal_hashes} with exactly {max_length} letters...')
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
            word = prefix
            for j in range(0, length - prefix_len):
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

def main():
    """
    Main function, called when the program is run.
    """
    # Setup arguments
    parser = argparse.ArgumentParser(description='Brute force searches for a password given a hash and a length.')
    parser.add_argument('hashes', metavar='HASH', type=str, nargs='+', help='the hash to search for')
    parser.add_argument('--max-length', metavar='MAX_LENGTH', type=int, default=8, help='the max length of the code')
    parser.add_argument('--min-length', metavar='MIN_LENGTH', type=int, default=1, help='the min length of the code')
    parser.add_argument('-p', '--prefix', metavar='PREFIX', type=str, default=None, help='the prefix to use for the code')
    parser.add_argument('-d', '--dict', metavar='DICT_FILE', type=str, help='the dictionary file to search')
    parser.add_argument('-o', '--outfile', metavar='OUTFILE', type=str, default='matches.txt', help='the file to write the results to')
    args = parser.parse_args()

    goal_hashes = args.hashes
    max_length = args.max_length
    min_length = args.min_length
    prefix = args.prefix
    dict_file = args.dict
    outfile = args.outfile

    matches = []

    start = time.time()
    if dict_file is None:
        print("Starting brute force search...")
        matches = brute_force_search(goal_hashes, max_length, min_length, prefix, outfile)
    else:
        print(f"Starting dictionary search using {dict_file}...")
        matches = dictionary_search(dict_file, goal_hashes, max_length, min_length, outfile)

    end = time.time()
    print(f'Found {len(matches)} matches in {(end - start):.2f}s.')
    #print('\n'.join(matches))

if __name__ == "__main__":
    main()

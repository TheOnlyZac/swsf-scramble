"""
search.py

This file contains the code for searching for a code given a hash and a length
"""
import os
import time
import argparse
from scramble import swsf_scramble

DEBUG = False

def dictionary_search(dict_file: str, goal_hashes: list, max_length: int = 8, min_length: int = 1, outfile: str = 'matches.txt') -> int:
    """
    Searches for a hash in a dictionary file.

    @param dict_file the dictionary file to search
    @param goal_hashes the list of hashes to search for
    @param max_length the max length of the words to check
    @param min_length the min length of the words to check
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
    Searches for a code by brute force.

    @param goal_hashes the list of hashes to search for
    @param max_length the max length of the codes to check
    @param min_length the min length of the codes to check
    @param prefix the prefix to use for the codes
    @param outfile the file to write the results to
    """
    matches = []
    num_matches = 0

    # Make sure prefix is valid
    if prefix is None:
        prefix = ''

    prefix_len = len(prefix)
    if prefix_len > max_length:
        print('Error: prefix is longer than max length.')
        return matches

    # Make sure max and min lengths are valid
    if max_length < min_length:
        print('Error: max length must be greater than or equal to min length.')
        return matches
    elif max_length < 0 or min_length < 0:
        print('Error: max length and min length must be greater than or equal to 0.')
        return matches
    elif max_length > 8 or min_length > 8:
        print('Warning: codes greater than 8 characters cannot be used in-game.')

    # Open the output file
    if outfile is not None:
        with open(outfile, 'w+', encoding='utf-8') as f:
            f.write(f'---- Hash collisions for {goal_hashes} of length {min_length}-{max_length} ----\n')

    # Calculate the number of possible codes
    num_possible_codes = 0
    for i in range(min_length - prefix_len, max_length - prefix_len + 1):
        num_possible_codes += 26**i
        if DEBUG:
            print(f'Length {i + prefix_len}: 26^{i} = {26**i:,} codes')

    # Print some info
    s = f'Searching for codes matching {goal_hashes}'
    if max_length == min_length:
        s += f'\n - Exactly {max_length} letters'
    else:
        s += f'\n - Between {min_length} and {max_length} letters'

    if prefix_len > 0:
        s += f'\n - Starting with "{prefix}"'

    print(f'{s}\nThere are {num_possible_codes:,} possible codes to check.')

    num_codes_checked = 0
    percent_done = 0
    start_time = time.time()
    for length in range(min_length, max_length + 1):
        for i in range(26**(length - prefix_len)):
            # Estimate time remaining every 100k codes
            if num_codes_checked > 0 and num_codes_checked % 100_000 == 0:
                percent_done = num_codes_checked / num_possible_codes

                now = time.time()
                wps = num_codes_checked / (now - start_time)
                codes_remaining = num_possible_codes - num_codes_checked
                time_remaining = codes_remaining / wps

                print(f'Progress: {percent_done * 100:.2f}% ({num_matches} matches found, ~{time_remaining:,.0f}s remaining)', end='\r')

            # Generate code
            code = prefix
            for j in range(0, length - prefix_len):
                code += chr(ord('a') + (i // (26**j)) % 26)

            # Scramble the code
            code_hash = swsf_scramble(code)
            if DEBUG:
                print(f'Checking {code} ({code_hash})')

            # Check the code against the goal hashes
            num_codes_checked += 1
            if code_hash in goal_hashes:
                matches.append(f'{code} ({code_hash})')
                num_matches += 1

                if outfile is not None:
                    with open(outfile, 'a+', encoding='utf-8') as f:
                        f.write(f'{code} ({code_hash})\n')

                if DEBUG:
                    print(f'Match found: {code} ({code_hash})')

    print(f'Results have been written to {outfile}.')
    return matches

def main():
    """
    Main function, called when the program is run.
    """
    # Setup arguments
    parser = argparse.ArgumentParser(description='Searches for a code given a hash and a length.')
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
        if DEBUG:
            print("Starting brute force search...")
        matches = brute_force_search(goal_hashes, max_length, min_length, prefix, outfile)
    else:
        print(f"Starting dictionary search using {dict_file}...")
        matches = dictionary_search(dict_file, goal_hashes, max_length, min_length, outfile)

    end = time.time()
    print(f'Found {len(matches)} matches in {(end - start):.2f}s.')

if __name__ == "__main__":
    main()

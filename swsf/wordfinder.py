"""
wordfinder.py

This file contains the code for finding valid English words in a list of strings.
"""
import argparse

def find_codes_containing_words(codes_file: str, dict_file: str, min_length: int = 0, outfile: str = None):
    """
    Finds valid English words in a list of strings.

    @param strings the list of strings to check
    """
    # Define a list of valid English words
    with open(dict_file, 'r', encoding='utf-8') as f:
        dict_words = [word.strip().lower() for word in f]

    with open(codes_file, 'r', encoding='utf-8') as f:
        codes = f.read().splitlines()

    # Toss out all dictionary words that are longer than the longest string or shorter than the minimum length
    max_code_length = max([len(code) for code in codes])
    dict_words = [word for word in dict_words if len(word) <= max_code_length and len(word) >= min_length]

    # Print some info
    print("Searching for words in the list of codes...")
    print(f'Max word length: {max_code_length}')
    print(f'Number of words in dictionary: {len(dict_words)}')

    # Check each string in the list
    matches = []
    for code in codes:
        #print(f'Checking {word} in {string}')
        for dict_word in dict_words:
            #print(f'Checking {dict_word} in {string}')
            # Check if the word is in the word list
            if dict_word in code:
                # If the word is in the list, print the string and break out of the loop
                if outfile is None:
                    print(f'{dict_word} in {code}')
                matches.append(f'{dict_word} in {code}')
                break

    if outfile is not None:
        print(f'Writing {len(matches)} matches to {outfile}')
        with open(outfile, 'w+', encoding='utf-8') as f:
            f.write(f'Codes from {codes_file} containing words from {dict_file} at least {min_length} letters:\n\n')
            for match in matches:
                f.write(f'{match}\n')

def reformat_strings_file(strings_file: str) -> None:
    """
    Reformats a list of strings to be one string per line.

    @param strings_file the file to reformat
    """
    with open(strings_file, 'r', encoding='utf-8') as f:
        strings = f.read().splitlines()
        # Make backup of original file
        with open(f'{strings_file}.bak', 'w+', encoding='utf-8') as f2:
            for string in strings:
                f2.write(f'{string}\n')

    with open(strings_file, 'w+', encoding='utf-8') as f:
        for string in strings:
            word = string.split()[0]
            f.write(f'{word}\n')

def main():
    """
    Finds strings in a list of hashes that contain valid words from the dictionary.
    """

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Finds codes in a list that contain valid words from the dictionary.')
    parser.add_argument('codes_file', help='the file containing the list of codes')
    parser.add_argument('dict_file', help='the file containing the dictionary')
    parser.add_argument('-l', '--min-length', type=int, default=0, help='the minimum length of a word to check for')
    parser.add_argument('-o', '--outfile', default='word_matches.txt', help='the file to write the matches to')

    args = parser.parse_args()
    codes_file = args.codes_file
    dict_file = args.dict_file
    min_length = args.min_length
    outfile = args.outfile

    reformat_strings_file(codes_file)

    # Find valid English words in the list of hashes
    find_codes_containing_words(codes_file, dict_file, min_length, outfile)

if __name__ == '__main__':
    main()

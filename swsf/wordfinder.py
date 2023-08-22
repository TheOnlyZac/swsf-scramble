"""
wordfinder.py

This file contains the code for finding valid English words in a list of strings.
"""
import sys

def find_strings_containing_words(strings_file, dict_file, min_length=0):
    """
    Finds valid English words in a list of strings.

    @param strings the list of strings to check
    """
    # Define a list of valid English words
    with open(dict_file, 'r', encoding='utf-8') as f:
        word_list = [word.strip().lower() for word in f]

    with open(strings_file, 'r', encoding='utf-8') as f:
        strings = f.read().splitlines()

    # Toss out all dictionary words that are longer than the longest string
    max_string_length = max([len(string) for string in strings])
    word_list = [word for word in word_list if len(word) <= max_string_length and len(word) >= min_length]

    # Check each string in the list
    for string in strings:
        # Split the string into individual words
        words = string.split()

        # Check each word in the string
        for word in words:
            for dict_word in word_list:
                # Check if the word is in the word list
                if dict_word in word:
                    # If the word is in the list, print the string and break out of the loop
                    print(string)
                    break

def reformat_strings_file(strings_file):
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

def main(argc, argv):
    """
    Finds strings in a list of hashes that contain valid words from the dictionary.
    """
    if argc == 1:
        print(f'Usage:\n\tpython {sys.argv[0]} STRINGS_FILE DICTIONARY_FILE')
        return

    # Read the dictionary file
    strings_file = argv[1]
    dict_file = argv[2]

    reformat_strings_file(strings_file)

    # Find valid English words in the list of hashes
    find_strings_containing_words(strings_file, dict_file, 4)

if __name__ == '__main__':
    main(len(sys.argv), sys.argv)

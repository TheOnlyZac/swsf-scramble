"""
gen_dict.py

This file contains the code for generating a dictionary file from an input file.
It takes all the words in the input file and writes them to the output file on
separate lines.
"""
import os
import argparse

def generate_dictionary(infile: str, outfile: str = None, encoding: str = 'utf-8') -> None:
    """
    Generates a dictionary file from an input file.

    @param infile the input file to read from
    @param outfile the output file to write to
    """
    if not os.path.isfile(infile):
        print(f'Error: {infile} is not a file.')
        return

    if outfile is None:
        outfile = infile + '.dict'

    with open(infile, 'r', encoding=encoding) as f:
        lines = f.read().splitlines()
        words = []
        for line in lines:
            # Replace all non-alphanumeric characters with spaces
            line = ''.join([c if c.isalnum() else ' ' for c in line])

            # Split the line into words and add them to the list
            words.extend(line.split())

    with open(outfile, 'w+', encoding='utf-8') as f:
        f.write('\n'.join(words))

def main():
    """
    Main function
    """
    parser = argparse.ArgumentParser(description='Generate a dictionary file from an input file.')
    parser.add_argument('infile', type=str, help='the input file to read from')
    parser.add_argument('-o', '--outfile', type=str, help='the output file to write to')
    parser.add_argument('-e', '--encoding', type=str, default='utf-8', help='the encoding of the input file')

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    encoding = args.encoding

    generate_dictionary(infile, outfile, encoding)

if __name__ == '__main__':
    main()

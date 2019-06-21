#!/usr/bin/env python3
import sys

import cson

def read_input(filename):
    with open(filename, 'rb') as infile:
        data = cson.load(infile)
    return data


if __name__ == '__main__':
    filename = sys.argv[1]
    input_data = read_input(filename)
    print(input_data)

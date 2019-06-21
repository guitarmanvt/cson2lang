#!/usr/bin/env python3
import sys
import json

import cson

from xmlish import C, RawDoc, X, Y

SPEC_VERSION = '1.0'  # XXX: Make this an argument?

def read_input(filename):
    with open(filename, 'rb') as infile:
        data = cson.load(infile)
    return data

def convert(data):
    doc = RawDoc()

    # Extract data bits into enclosing context.
    lang_id = data['scopeName'].split('.')[-1]
    name = data['name']

    # Convert in enclosed functions for readability.
    def header():
        doc.add(Y('xml', version='1.0', encoding='UTF-8'))
        doc.add(C('Syntax highlighting for the {} language'.format(name)))

    def language():
        lang = doc.add('language', id=lang_id, name=name, version=SPEC_VERSION, section='Sources')
        metadata = lang.add('metadata')
        # metadata.add('property', name='mimetypes').text('XXX')  # XXX: CSON doesn't support mimetypes?


    # Put it all together.
    header()
    language()
    return doc


if __name__ == '__main__':
    filename = sys.argv[1]
    input_data = read_input(filename)
    with open(filename + '.json', 'w') as json_debug_file:
        json.dump(input_data, json_debug_file)
    doc = convert(input_data)
    print(str(doc))

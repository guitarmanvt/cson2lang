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


# Using globals cuz lazy.
data = {} # input data from CSON
doc = RawDoc()  # output XML structure to be dumped as lang spec

# Accessor functions/lambdas for terseness.
lang_id = lambda : data['scopeName'].split('.')[-1]
name = lambda : data['name']
globs = lambda : ';'.join('*.{}'.format(x) for x in data['fileTypes'])
repo = lambda : data['repository']

def comment_markers():
    return [(d['begin'], d['end']) for d in
            repo().get('comment', {}).get('patterns', [])]

line_comments = lambda : [c[0] for c in comment_markers() if c[1] == '\\n']
block_comments = lambda : [b for b in comment_markers() if b[1] != '\\n']
line_comment_start = lambda : line_comments()[0] if line_comments() else None
block_comment_start = lambda : block_comments()[0][0] if block_comments() else None
block_comment_end = lambda : block_comments()[0][1] if block_comments() else None

# Converter functions.
def header():
    doc.add(Y('xml', version='1.0')) #, encoding='UTF-8')) - gets sorted wrong :P
    doc.add(C('Syntax highlighting for the {} language'.format(name())))

def language():
    lang = doc.add('language', id=lang_id(), name=name(), version=SPEC_VERSION, section='Sources')
    metadata(lang)

def metadata(lang):
    mdata = lang.add('metadata')
    # mdata.add('property', name='mimetypes').text('XXX')  # XXX: CSON doesn't support mimetypes?
    mdata.add('property', name='globs').text(globs())
    mdata.add('property', name='line-comment-start').text(line_comment_start())
    mdata.add('property', name='block-comment-start').text(block_comment_start())
    mdata.add('property', name='block-comment-end').text(block_comment_end())

def convert():
    # Put it all together.
    header()
    language()


if __name__ == '__main__':
    filename = sys.argv[1]
    data.update(read_input(filename))
    with open(filename + '.json', 'w') as json_debug_file:
        json.dump(data, json_debug_file)
    convert()
    print(str(doc))

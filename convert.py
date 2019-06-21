#!/usr/bin/env python3
import re
import sys
import json

import cson

from xmlish import C, RawDoc, X, Y

SPEC_VERSION = '2.0'  # Must be 2.0 per the spec
NAME_FUDGE = {  # cson name: lang name
    'kwString': 'keyword',
    'array': 'skip',
    'interpolation': 'skip',
    'object': 'skip',
    'heredoc': 'skip',
}

def read_input(filename):
    with open(filename, 'rb') as infile:
        data = cson.load(infile)
    return data

# Using globals cuz lazy.
data = {} # input data from CSON
doc = RawDoc()  # output XML structure to be dumped as lang spec
# References to parts of the XML output structure:
lang = None
styles = None

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
    doc.add(Y('xml', version="1.0", encoding='UTF-8')).attribute_order('version', 'encoding')
    doc.add(C('Syntax highlighting for the {} language'.format(name())))


def language():
    global lang
    lang = doc.add('language', id=lang_id(), name=name(), version=SPEC_VERSION, section='Sources')
    metadata()
    styles()
    definitions()


def metadata():
    mdata = lang.add('metadata')
    # mdata.add('property', name='mimetypes').text('XXX')  # XXX: CSON doesn't support mimetypes?
    mdata.add('property', name='globs').text(globs())
    mdata.add('property', name='line-comment-start').text(line_comment_start())
    mdata.add('property', name='block-comment-start').text(block_comment_start())
    mdata.add('property', name='block-comment-end').text(block_comment_end())


def add_style(id, name=None, map=None):
    name = name if name else id.title()
    map = map if map else 'def:{}'.format(id)
    styles.add('style', id=id, name=name, **{'map-to': map}).attribute_order('id', 'name')


def styles():
    global styles
    mapto = lambda x: {'map-to': x}
    styles = lang.add('styles')


def definitions():
    styleref = lambda x: {'style-ref': x}

    defs = lang.add('definitions')
    top = defs.add('context', id=lang_id()).add('include')

    # Comments
    safestars = lambda x: x.replace('*', '\\*')
    add_style('comment')
    for n, (start, end) in enumerate(comment_markers()):
        end = '$' if end == '\\n' else end
        start = safestars(start)
        end = safestars(end)
        name = 'comment_type_{}'.format(n)
        ctx = top.add('context', id=name, **styleref('comment'))
        ctx.add('start').text(start)
        ctx.add('end').text(end)

    for name, details in repo().items():
        name = NAME_FUDGE.get(name, name)
        if name == 'skip':
            continue

        # Simple regexes.
        match = details.get('match')
        if match:
            ctx = top.add('context', id=name, **styleref(name))
            ctx.add('match', extended='true').text(match)
            add_style(name)
            continue

        # Start/end definitions
        start = details.get('begin')
        end = details.get('end')
        if start and end:
            ctx = top.add('context', id=name, **styleref(name))
            ctx.add('start').text(start)
            ctx.add('end').text(end)
            add_style(name)
            continue


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

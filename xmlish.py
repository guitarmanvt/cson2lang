"""Dirt-simple XML structure building, without the nasties.

Simplifications/limitations:
- XML comments are only allowed as siblings to other tags and strictly formatted.
- Internal Text is allowed, but cannot be intermixed with children or comments.
- You want a tag with no attributes, you gotta do `X({'tagname': {}})`

Yeah, I know it's limited.
"""
import logging
from textwrap import dedent, indent

logging.basicConfig(filename='output.log',level=logging.DEBUG)


def log(object_type, output):
    logging.debug('{} object'.format(object_type))
    logging.debug('\n  :'.join(output))


class C(object):
    def __init__(self, comment):
        self.comment = dedent(comment)

    def to_xml_lines(self, margin=0, *args, **kwargs):
        output = []
        spaces = ' ' * margin
        output.append('{}<!--'.format(spaces))
        output.append(indent(self.comment, ' ' * margin))
        output.append('{}-->'.format(spaces))
        log('C', output)
        return output

class X(object):
    def __init__(self, tagname, text=None, **attributes):
        self.tagname = tagname
        self.text = text
        self.attributes = attributes if attributes else dict()
        self.children = []

    def _formatted_attributes(self):
        if self.attributes:
            kvpairs = ('{}="{}"'.format(attr, val) for attr, val in sorted(self.attributes.items()))
            formatted_attrs = ' ' + ' '.join(kvpairs)
        else:
            formatted_attrs = ''
        return formatted_attrs

    def add(self, what, **attributes):
        if self.text:
            raise ValueError('Node has text and cannot have children.')
        if type(what) in [C, X]:
            child = what
        elif type(what) in [Y]:
            raise ValueError('X node cannot accept Y children.')
        else:
            child = X(what, **attributes)
        self.children.append(child)
        return child

    def to_xml_lines(self, margin=0, indent=2):
        output = []
        formatted_attrs = self._formatted_attributes()
        spaces = ' ' * margin
        if self.children or self.text:
            output.append('{}<{}{}>'.format(spaces, self.tagname, formatted_attrs))
            for child in self.children:
                output.extend(child.to_xml_lines(margin + indent, indent))
            output.append('{}</{}>'.format(spaces, self.tagname))
        else:
            # Self-closing tag.
            output.append('{}<{}{}/>'.format(spaces, self.tagname, formatted_attrs))
        log('X', output)
        return output

    def __str__(self):
        return '\n'.join(self.to_xml_lines())


class Y(X):
    def add(self, *args, **kwargs):
        raise ValueError('Y cannot have children.')

    def to_xml_lines(self, margin=0, indent=2):
        output = []
        formatted_attrs = self._formatted_attributes()
        spaces = ' ' * margin
        # Special self-closing tag.
        output.append('{}<?{}{}?>'.format(spaces, self.tagname, formatted_attrs))
        log('Y', output)
        return output


class RawDoc(dict):
    def __init__(self):
        self.children = []

    def add(self, what, **attributes):
        if type(what) in [C, Y, X]:
            child = what
        else:
            child = X(what, **attributes)
        self.children.append(child)
        return child

    def to_xml_lines(self, margin=0, indent=2):
        output = []
        spaces = ' ' * margin
        if self.children or self.text:
            for child in self.children:
                output.extend(child.to_xml_lines(margin, indent))
        log('RawDoc', output)
        return output

    def __str__(self):
        return '\n'.join(self.to_xml_lines())

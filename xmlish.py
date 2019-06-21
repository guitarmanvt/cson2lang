"""Dirt-simple XML structure building, without the nasties.

Simplifications/limitations:
- XML comments are only allowed as siblings to other tags and strictly formatted.
- Internal Text is allowed, but cannot be intermixed with children or comments.
- Attributes get scrambled by Python's key hashing. If order is really important,
  call `.attribute_order()` after object construction.

Yeah, I know it's limited.
"""
from collections import OrderedDict
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
    def __init__(self, tagname, **attributes):
        self.tagname = tagname
        self._text = None
        self.attributes = attributes if OrderedDict(**attributes) else OrderedDict()
        self.children = []
        self._aorder = []

    def _formatted_attributes(self):
        if self.attributes:
            if self._aorder:
                # Return attributes in a specific order. Required by some Schema.
                ordered_attrs = []
                for attr in self._aorder:
                    val = self.attributes.get(attr)
                    if val:
                        ordered_attrs.append((attr, val))
                unordered = [key for key in self.attributes.keys() if key not in self._aorder]
                ordered_attrs.extend((key, self.attributes[key]) for key in sorted(unordered))
            else:
                # sort alphabetically
                ordered_attrs = sorted(self.attributes.items())
            kvpairs = ('{}="{}"'.format(attr, val) for attr, val in ordered_attrs)
            formatted_attrs = ' ' + ' '.join(kvpairs)
        else:
            formatted_attrs = ''
        return formatted_attrs

    def add(self, what, **attributes):
        if self._text:
            raise ValueError('Node has text and cannot have children.')
        if type(what) in [C, X]:
            child = what
        elif type(what) in [Y]:
            raise ValueError('X node cannot accept Y children.')
        else:
            child = X(what, **attributes)
        self.children.append(child)
        return child

    def text(self, text):
        if self.children:
            raise ValueError('Node has children and cannot have text.')
        self._text = text
        return self  # in fluent style

    def attribute_order(self, *order):
        if self._aorder:
            raise ValueError('attribute order is already set')
        self._aorder = order[:]
        return self  # in fluent style

    def to_xml_lines(self, margin=0, indent=2):
        output = []
        formatted_attrs = self._formatted_attributes()
        spaces = ' ' * margin
        if self._text:
            output.append('{}<{}{}>{}</{}>'.format(spaces, self.tagname, formatted_attrs, self._text, self.tagname))
        elif self.children:
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

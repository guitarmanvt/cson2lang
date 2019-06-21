"""Dirt-simple XML structure building, without the nasties.

Simplifications/limitations:
- XML comments are only allowed as siblings to other tags and strictly formatted.
- Internal Text is allowed, but cannot be intermixed with children or comments.
- You want a tag with no attributes, you gotta do `X({'tagname': {}})`

Yeah, I know it's limited.
"""
from textwrap import dedent, indent

class C(object):
    def __init__(self, comment):
        self.comment = dedent(comment)

    def to_xml_lines(self, margin=0):
        output = []
        spaces = ' ' * margin
        output.append('{}<!--'.format(spaces))
        output.append(indent(self.comment, ' ' * margin))
        output.append('{}-->'.format(spaces))
        return output

class X(dict):
    def __init__(self, tagname, text=None, **attributes):
        self.tagname = tagname
        self.text = text
        self.attributes = attributes if attributes else dict()
        self.children = []

    def add(self, what, **attributes):
        if self.text:
            raise AttributeError('Node has text and cannot have children.')
        if type(what) in [X, C]:
            child = what
        else:
            child = X(what, **attributes)
        self.children.append(child)
        return child

    def to_xml_lines(self, margin=0, indent=2):
        output = []
        if self.attributes:
            kvpairs = ('{}="{}"'.format(attr, val) for attr, val in sorted(self.attributes.items()))
            formatted_attrs = ' ' + ' '.join(kvpairs)
        else:
            formatted_attrs = ''
        spaces = ' ' * margin
        if self.children or self.text:
            output.append('{}<{}{}>'.format(spaces, self.tagname, formatted_attrs))
            for child in self.children:
                output.extend(child.to_xml_lines(margin + indent, indent))
            output.append('{}</{}>'.format(spaces, self.tagname))
        else:
            # Self-closing tag.
            output.append('{}<{}{}/>'.format(spaces, self.tagname, formatted_attrs))
        return output

    def __str__(self):
        return '\n'.join(self.to_xml_lines())

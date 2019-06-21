"""Dirt-simple XML structure building, without the nasties.

Simplifications/limitations:
- No XML comments are allowed.
- No internal text is allowed.
- You want a tag with no attributes, you gotta do `X({'tagname': {}})`

Yeah, I know it's limited.
"""


class X(dict):
    def __init__(self, tagname, **attributes):
        self.tagname = tagname
        self.attributes = attributes if attributes else dict()
        self.children = []

    def add(self, what, **attributes):
        if type(what) == X:
            child = what
        else:
            child = X(what, **attributes)
        self.children.append(child)
        return child

    def to_xml_lines(self, margin=0, indent=2):
        output = []
        if self.attributes:
            kvpairs = ('{}="{}"'.format(attr, val) for attr, val in self.attributes.items())
            formatted_attrs = ' ' + ' '.join(kvpairs)
        else:
            formatted_attrs = ''
        spaces = ' ' * margin
        output.append('{}<{}{}>'.format(spaces, self.tagname, formatted_attrs))
        for child in self.children:
            output.extend(child.to_xml_lines(margin + indent, indent))
        output.append('{}</{}>'.format(spaces, self.tagname))
        return output

    def __str__(self):
        return '\n'.join(self.to_xml_lines())

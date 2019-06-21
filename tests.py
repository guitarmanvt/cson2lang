from textwrap import dedent
import unittest

from xmlish import X

class TestX(unittest.TestCase):

    def test_single_tag_returns_no_attributes_or_children(self):
        self.assertEqual(str(X('body')), '<body>\n</body>')

    def test_single_tag_with_attributes_no_children(self):
        self.assertEqual(str(X('body', shave='haircut')), '<body shave="haircut">\n</body>')

    def test_tag_no_attributes_one_child(self):
        x = X('body')
        x.add('beach')
        self.assertEqual(''.join(x.to_xml_lines(0, 0)), '<body><beach></beach></body>')


if __name__ == '__main__':
    unittest.main()

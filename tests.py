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

    def test_nested_with_attributes(self):
        x = X('vacation', style='family', source='contest')
        x.add('destination', city='Venice', country='Italy')
        x.add('activities').add('guided-tour', vehicle='gondola')
        self.assertEqual(str(x), dedent('''
            <vacation style="family" source="contest">
              <destination city="Venice" country="Italy">
              </destination>
              <activities>
                <guided-tour vehicle="gondola">
                </guided-tour>
              </activities>
            </vacation>
        ''').strip())

if __name__ == '__main__':
    unittest.main()

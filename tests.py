from textwrap import dedent
import unittest

from xmlish import X

class TestX(unittest.TestCase):

    def test_single_tag_returns_no_attributes_or_children(self):
        self.assertEqual(str(X('body')), '<body/>')

    def test_single_tag_with_attributes_no_children(self):
        self.assertEqual(str(X('body', shave='haircut')),
                         '<body shave="haircut"/>')

    def test_tag_no_attributes_one_child(self):
        x = X('body')
        x.add('beach')
        self.assertEqual(str(x), dedent('''
            <body>
              <beach/>
            </body>
        ''').strip())

    def test_nested_with_attributes(self):
        x = X('vacation', style='family', source='contest')
        x.add('destination', city='Venice', country='Italy')
        # NOTE: This is a "fluent" usage:
        x.add('activities').add('guided-tour', vehicle='gondola')
        self.assertEqual(str(x), dedent('''
            <vacation source="contest" style="family">
              <destination city="Venice" country="Italy"/>
              <activities>
                <guided-tour vehicle="gondola"/>
              </activities>
            </vacation>
        ''').strip())

if __name__ == '__main__':
    unittest.main()

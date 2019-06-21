from textwrap import dedent
import unittest

from xmlish import C, RawDoc, X, Y

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

    def test_tag_with_text(self):
        x = X('story')
        x.text('It was a dark and stormy night...')
        self.assertEqual(str(x), '<story>It was a dark and stormy night...</story>')


class TestRawDocAndY(unittest.TestCase):
    def test_rawdoc_with_y_and_comment(self):
        doc = RawDoc()
        doc.add(Y('xml', version='1.0', encoding='UTF-8'))
        doc.add(C(dedent('''
            This is a
            multi-line
            comment.
        ''').strip()))
        self.assertEqual(str(doc), dedent('''
            <?xml encoding="UTF-8" version="1.0"?>
            <!--
            This is a
            multi-line
            comment.
            -->
        ''').strip())

if __name__ == '__main__':
    unittest.main()

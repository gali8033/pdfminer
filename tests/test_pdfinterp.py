import unittest
import tools.pdf2txt


class TestEmptyPdf(unittest.TestCase):

    def testEmpty(self):

        argv = ['pdf2txt.py', '-o', 'samples/testxml.xml', '-t', 'xml',
                'samples/empty-pdf.pdf']
        self.assertEqual(tools.pdf2txt.setOptionsAndConvert(argv), "")


if __name__ == '__main__':
    unittest.main()

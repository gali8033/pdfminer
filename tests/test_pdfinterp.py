import unittest
import tools.pdf2txt
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import XMLConverter


class TestEmptyPdf(unittest.TestCase):

    def testEmpty(self):
        obj = PDFPageInterpreter(None, None)
        self.assertEqual(obj.execute([]), None)


if __name__ == '__main__':
    unittest.main()

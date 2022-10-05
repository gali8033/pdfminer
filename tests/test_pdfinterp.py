import unittest
from pdfminer.pdfinterp import PDFPageInterpreter


class TestEmptyPdf(unittest.TestCase):

    def testEmpty(self):
        obj = PDFPageInterpreter(None, None)
        self.assertEqual(obj.execute([]), None)


if __name__ == '__main__':
    unittest.main()

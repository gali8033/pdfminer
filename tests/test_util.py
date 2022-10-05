import unittest
import pdfminer.utils


class TestUtils(unittest.TestCase):

    def testRightbbox2str(self):
        bbox = (25, 50, 30, 60)
        rightbbox = '30.000,60.000'
        self.assertEqual(rightbbox, pdfminer.utils.rightbbox2str(bbox))

    def testLeftbbox2str(self):
        bbox = (25, 50, 30, 60)
        leftbbox = '25.000,50.000'
        self.assertEqual(leftbbox, pdfminer.utils.leftbbox2str(bbox))

    def test_q(self):
        self.assertEqual(pdfminer.utils.q('&'), '&amp;')
        self.assertEqual(pdfminer.utils.q('<'), '&lt;')
        self.assertEqual(pdfminer.utils.q('>'), '&gt;')
        self.assertEqual(pdfminer.utils.q('"'), '&quot;')
         


if __name__ == '__main__':
    unittest.main()

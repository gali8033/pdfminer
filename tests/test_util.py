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

    def testQNoSpecialChars(self):
        input_string = 'Test string without any special chars'
        output_string = pdfminer.utils.q(input_string)
        self.assertEqual(input_string, output_string)

    def testQSingleSpecialChars(self):
        input_string = 'We now test the char &'
        expected_output = 'We now test the char &amp;'
        output_string = pdfminer.utils.q(input_string)
        self.assertEqual(expected_output, output_string)

        input_string = 'We now test the char <'
        expected_output = 'We now test the char &lt;'
        output_string = pdfminer.utils.q(input_string)
        self.assertEqual(expected_output, output_string)

        input_string = 'We now test the char >'
        expected_output = 'We now test the char &gt;'
        output_string = pdfminer.utils.q(input_string)
        self.assertEqual(expected_output, output_string)

        input_string = 'We now test the char "'
        expected_output = 'We now test the char &quot;'
        output_string = pdfminer.utils.q(input_string)
        self.assertEqual(expected_output, output_string)

    def testQMultipleSpecialChars(self):
        input_string = 'We now test the chars & <> "'
        expected_output = 'We now test the chars &amp; &lt;&gt; &quot;'
        output_string = pdfminer.utils.q(input_string)
        self.assertEqual(expected_output, output_string)


if __name__ == '__main__':
    unittest.main()

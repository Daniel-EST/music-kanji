import unittest

from crawler.utils import parse_csv


class TestUtils(unittest.TestCase):
    def test_parse_csv(self):
        csv_string = 'column_1,column_2,column_3\na,b,c'
        result = parse_csv(csv_string)
        self.assertEqual(list(result), [{'column_1': 'a',
                                         'column_2': 'b',
                                         'column_3': 'c'}])

        csv_string = 'column_1,column_2,column_3\na,b,c\nd,e,f'
        result = parse_csv(csv_string)
        self.assertEqual(list(result), [{'column_1': 'a',
                                         'column_2': 'b',
                                         'column_3': 'c'},
                                        {'column_1': 'd',
                                         'column_2': 'e',
                                         'column_3': 'f'}])


if __name__ == '__main__':
    unittest.main()

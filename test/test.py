import unittest
import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dph_generator
from dph_generator import DphGenerator

class TestDphGenerator(unittest.TestCase):

    def setUp(self):
        os.system('rm -f *.xml')

    def assertFilesEqual(self, expected_file_name, actual_file_name):
        with open(expected_file_name, 'r') as expected_file:
            expected = expected_file.read()

            with open(actual_file_name, 'r') as actual_file:
                self.assertEqual(expected, actual_file.read())

    def test_generate_declaration_for_stepan(self):
        dph_generator.main(['-t', '10', '-c', 'config_stepan'], datetime(2014, 10, 4, 6, 8, 30))

        self.assertFilesEqual('DPHSHV-1234561234-20141004-060830.xml_orig',
                              'DPHSHV-1234561234-20141004-060830.xml')

        self.assertFilesEqual('DPHDP3-1234561234-20141004-060830.xml_orig',
                              'DPHDP3-1234561234-20141004-060830.xml')

    def test_generate_declaration_for_kun(self):
        dph_generator.main(['-t', '999999', '-c', 'config_kun'], datetime(2014, 11, 30, 2, 48, 44))

        self.assertFilesEqual('DPHDP3-1212121207-20141130-024844.xml_orig',
                              'DPHDP3-1212121207-20141130-024844.xml')

        self.assertFilesEqual('DPHSHV-1212121207-20141130-024844.xml_orig',
                              'DPHSHV-1212121207-20141130-024844.xml')

    def test_generate_file_name(self):
        g = dph_generator.DphGenerator(datetime(1978, 6, 13, 1, 2, 3))
        g.read_config('config_stepan')

        self.assertEqual('DPHDP3-1234561234-19780613-010203', g.get_file_name('DP3'))
        self.assertEqual('DPHSHV-1234561234-19780613-010203', g.get_file_name('SHV'))

        g = dph_generator.DphGenerator(datetime(2014, 10, 4, 6, 8, 30))
        g.read_config('config_stepan')

        self.assertEqual('DPHDP3-1234561234-20141004-060830', g.get_file_name('DP3'))
        self.assertEqual('DPHSHV-1234561234-20141004-060830', g.get_file_name('SHV'))


    def test_format_submission_date(self):
        d = datetime(2012, 10, 15)
        self.assertEqual('15.10.2012', DphGenerator(d).format_submission_date())

    def test_get_quarter(self):
        self.assertEqual(1, DphGenerator(datetime(2013, 1, 26)).get_quarter())
        self.assertEqual(4, DphGenerator(datetime(2013, 1, 1)).get_quarter())
        self.assertEqual(4, DphGenerator(datetime(2013, 12, 31)).get_quarter())
        self.assertEqual(1, DphGenerator(datetime(2013, 4, 25)).get_quarter())
        self.assertEqual(3, DphGenerator(datetime(2013, 10, 4)).get_quarter())
        self.assertEqual(2, DphGenerator(datetime(2013, 4, 30)).get_quarter())

    def test_get_year(self):
        self.assertEqual(2013, DphGenerator(datetime(2013, 1, 26)).get_year())
        self.assertEqual(2012, DphGenerator(datetime(2013, 1, 1)).get_year())
        self.assertEqual(2013, DphGenerator(datetime(2013, 12, 31)).get_year())
        self.assertEqual(2013, DphGenerator(datetime(2013, 4, 25)).get_year())
        
if __name__ == '__main__':
    unittest.main()


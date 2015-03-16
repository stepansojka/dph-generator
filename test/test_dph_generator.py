# coding=utf-8

import pytest
import os
import sys
from datetime import datetime
import xml.etree.ElementTree as et

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import dph_generator
from dph_generator import DphGenerator

def setup_method(self, method):
    os.system('rm -f *.xml')

def compare_files(filename_expected, filename_actual):
    expected = open(filename_expected).read()
    actual = open(filename_actual).read()
    assert expected == actual

def test_generate_declaration_for_stepan():
    dph_generator.main(['-t', '10', '-c', 'config_stepan'], datetime(2014, 10, 4, 6, 8, 30))


    compare_files('DPHSHV-1234561234-20141004-060830.xml_orig',
                  'DPHSHV-1234561234-20141004-060830.xml')

    compare_files('DPHDP3-1234561234-20141004-060830.xml_orig',
                  'DPHDP3-1234561234-20141004-060830.xml')

def test_generate_declaration_for_kun():
    dph_generator.main(['-t', '999999', '-c', 'config_kun'], datetime(2014, 11, 30, 2, 48, 44))

    compare_files('DPHDP3-1212121207-20141130-024844.xml_orig',
                  'DPHDP3-1212121207-20141130-024844.xml')

    compare_files('DPHSHV-1212121207-20141130-024844.xml_orig',
                  'DPHSHV-1212121207-20141130-024844.xml')

def test_generate_file_name():
    g = DphGenerator(datetime(1978, 6, 13, 1, 2, 3))
    g.read_config('config_stepan')

    assert 'DPHDP3-1234561234-19780613-010203' ==  g.get_file_name('DP3')
    assert 'DPHSHV-1234561234-19780613-010203' ==  g.get_file_name('SHV')

    g = dph_generator.DphGenerator(datetime(2014, 10, 4, 6, 8, 30))
    g.read_config('config_stepan')

    assert 'DPHDP3-1234561234-20141004-060830' == g.get_file_name('DP3')
    assert 'DPHSHV-1234561234-20141004-060830' == g.get_file_name('SHV')


def test_format_submission_date():
    d = datetime(2012, 10, 15)
    assert '15.10.2012' == DphGenerator(d).format_submission_date()

@pytest.mark.parametrize("input,expected", [
    ((2013, 1,  26),  1),
    ((2013, 1,   1),  4),
    ((2013, 12, 31),  4),
    ((2013, 4,  25),  1),
    ((2013, 10,  4),  3),
    ((2013, 4,  30),  2)
])
def test_get_quarter(input, expected):
    assert expected == DphGenerator(datetime(*input)).get_quarter()

@pytest.mark.parametrize("input,expected", [
    ((2013, 1,  26),  2013),
    ((2013, 1,   1),  2012),
    ((2013, 12, 31),  2013),
    ((2013, 4,  25),  2013)
])
def test_get_year(input, expected):
    assert expected == DphGenerator(datetime(*input)).get_year()
        

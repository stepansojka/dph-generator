#!/usr/bin/python

import string
import md5
import sys
import argparse
import datetime
import os
import ConfigParser

DEFAULT_CFG = '~/.dph_generator'
DEFAULT_CFG_FILE = os.path.expanduser(DEFAULT_CFG)

DEADLINE_PERIOD_DAYS = 25

class DphGenerator:
    def __init__(self, dt):
        self.dt = dt
        self.mapping = {}
        self.add_dates()

    def add_dates(self):
        self.mapping['quarter'] = self.get_quarter()
        self.mapping['year'] = self.get_year()
        self.mapping['submission_date'] = self.format_submission_date()

    def get_year(self):
        d = self.dt - datetime.timedelta(days = DEADLINE_PERIOD_DAYS)
        return d.year

    def get_quarter(self):
        d = self.dt - datetime.timedelta(days = DEADLINE_PERIOD_DAYS)
        return ((d.month - 1) / 3) + 1

    def format_submission_date(self):
        return self.dt.strftime('%d.%m.%Y')

    def read_config(self, config_file):
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)
        self.mapping.update(config_dict(config_parser, 'taxpayer'))

    def set_amount(self, amount):
        self.mapping['amount'] = amount

    def write_output_file(self, doctype):
        file_name = self.get_file_name(doctype)
        self.mapping['file'] = file_name
        with open(file_name + '.xml', 'w') as f:
            f.write(self.generate_document(doctype))

    def get_file_name(self, doctype):
        timestamp = self.dt.strftime('%Y%m%d-%H%M%S')
        return 'DPH%s-%s-%s' % (doctype, self.mapping['vat_no'], timestamp)

    def generate_document(self, doctype):
        doc = self.substitute_in_template(doctype)
        self.add_document_params(doc)
        return self.substitute_in_template('pisemnost')

    def add_document_params(self, doc):
        self.mapping['doc'] = doc
        self.mapping['len'] = len(doc)
        self.mapping['digest'] = md5.new(doc).hexdigest()

    def substitute_in_template(self, template):
        with open(get_template_file_name(template), 'r') as template_file:
            t = string.Template(template_file.read())
            return t.substitute(self.mapping)

def get_template_file_name(template):
    return os.path.join(os.path.dirname(__file__), 'templates', template + '.tpl')

def config_dict(config, section):
    d = {}
    options = config.options(section)
    for option in options:
        d[option] = config.get(section, option)

    return d

def parse_args(argv):
    parser = argparse.ArgumentParser(description='DPHSHV and DPHDP3 xml file generator.')

    parser.add_argument('-t','--total', type=int,
                        help='total declared amount in czk', required=True)
    parser.add_argument('-c','--config_file',
                        help='config file. Default is %s, see examples in the test directory.' % DEFAULT_CFG, default=DEFAULT_CFG_FILE)
    args = parser.parse_args(argv)

    if not os.path.isfile(args.config_file):
        print 'Config file %s does not exist.' % args.config_file
        print 'You can create one from one of the samples in the test directory.'
        exit(1)

    return args

def main(argv, dt):
    args = parse_args(argv)

    generator = DphGenerator(dt)
    generator.set_amount(args.total)
    generator.read_config(args.config_file)

    generator.write_output_file('SHV')
    generator.write_output_file('DP3')

if __name__ == '__main__':
    main(sys.argv[1:], datetime.datetime.now())


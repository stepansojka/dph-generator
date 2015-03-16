import glob
import os
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'dph-generator',
    packages = ['dph_generator'],
    version = '0.0.1',
    description = 'DPH Generator',
    long_description = 'DPH Generator.',
    license = 'MIT',
    author = 'Stepan Sojka',
    author_email = 'stepansojka@countermail.com',
    url = 'http://github.com/stepansojka/dph-generator',
    keywords = ['Tax DPH VAT CZ'],
    package_dir={'': 'src'},
#    install_requires = ['six'],
    py_modules=[splitext(basename(i))[0] for i in glob.glob('src/*.py')],
    classifiers = [
        'Topic :: Office/Business :: Financial',
        'Topic :: Utilities',
#        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython'
        ]
)

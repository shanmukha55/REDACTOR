import redactor as rd
from argparse import Namespace

def test_write():
    redacted_terms = ['Norman', 'Oklahoma']
    count = 2
    file = 'test1.txt'
    args = Namespace(input=[], names=True, dates=True, phones=True, genders=True, address=True, concept=["'kids'"], output="'files'", stats='stdout')
    rd.write_tostatfile(redacted_terms, count, file, args)
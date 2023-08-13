import pytest
import redactor as rd
from argparse import Namespace

def test_empty_input():
    with pytest.raises(SystemExit) as e:
        args = Namespace(input=[], names=True, dates=True, phones=True, genders=True, address=True, concept=["'kids'", "'phone'"], output="'files'", stats='stderr')
        rd.get_files(args)
    assert e.type == SystemExit
    assert e.value.code == 0

def test_get_files():
    args = Namespace(input=["'*.txt'"], names=True, dates=True, phones=True, genders=True, address=True, concept=["'kids'", "'phone'"], output="'files'", stats='stderr')
    files = rd.get_files(args)
    assert len(files) != 0



import redactor as rd
from argparse import Namespace

def test_output():
    complete_data = '\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588\u2588\u2588 was an American professional basketball player born in \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588. \u2588\u2588 was born on \u2588\u2588 \u2588\u2588\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588. \u2588\u2588\u2588 wife name is \u2588\u2588\u2588\u2588\u2588\u2588\u2588. \u2588\u2588\u2588 phone number is not \u2588\u2588\u2588 \u2588\u2588\u2588 \u2588\u2588\u2588\u2588.'
    files = 'test1.txt'
    args = Namespace(input=[], names=True, dates=True, phones=True, genders=True, address=True, concept=["'kids'"], output="'files'", stats='stdout')
    rd.output(args, complete_data, files)
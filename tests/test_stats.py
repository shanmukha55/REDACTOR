import redactor as rd
import warnings
from argparse import Namespace

def test_stats():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    args = Namespace(input=[], names=True, dates=True, phones=True, genders=True, address=True, concept=["'kids'"], output="'files'", stats='stderr')
    text = 'Kobe Bryant was an American professional basketball player born in Philadelphia. He was born on 23 August 1978. His wife name is Vanessa. They have 4 kids. His phone number is not 123 456 7890.'
    file = 'test1.txt'
    final_data = rd.stats(args, text, file)
    result = '\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588\u2588\u2588 was an American professional basketball player born in \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588. \u2588\u2588 was born on \u2588\u2588 \u2588\u2588\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588. \u2588\u2588\u2588 wife name is \u2588\u2588\u2588\u2588\u2588\u2588\u2588. \u2588\u2588\u2588 phone number is not \u2588\u2588\u2588 \u2588\u2588\u2588 \u2588\u2588\u2588\u2588.'
    assert final_data == result
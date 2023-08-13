import redactor as rd
from argparse import Namespace
import warnings

def test_redact_concepts():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    text = 'They have 4 kids. Kobe\'s wife name is Vanessa.'
    arg = Namespace(input=[], names=True, dates=True, phones=True, genders=True, address=True, concept=["'kids'"], output="'files'", stats='stderr')
    temp = 'They have 4 kids. Kobe\'s wife name is Vanessa.'
    expected,concepts,count = rd.redact_concepts(text, arg, temp)
    assert count == 1
    assert concepts == [('They have 4 kids.',0, 17,"'kids'")]
    assert expected == 'Kobe\'s wife name is Vanessa.'

def test_redact_multiple_concepts():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    text = 'Kobe\'s wife name is Vanessa. They have 4 kids. Kobe Bryant phone number is not 405-258-4568'
    arg = Namespace(input=[], names=True, dates=True, phones=True, genders=True, address=True, concept=["'kids'", "'phone'"], output="'files'", stats='stderr')
    temp = 'Kobe\'s wife name is Vanessa. They have 4 kids. Kobe Bryant phone number is not 405-258-4568'
    expected,concepts,count = rd.redact_concepts(text, arg, temp)
    assert count == 2
    assert concepts == [('They have 4 kids.',29, 46,"'kids'"),('Kobe Bryant phone number is not 405-258-4568',47, 91,"'phone'")]
    assert expected == 'Kobe\'s wife name is Vanessa.'
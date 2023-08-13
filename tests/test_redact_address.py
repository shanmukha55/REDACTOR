import redactor as rd
import warnings

def test_redact_address():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    text = 'Kobe Bryant was an American professional basketball player born in Philadelphia.'
    result = 'Kobe Bryant was an American professional basketball player born in \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588.'
    expected,address_list,count = rd.redact_address(text)
    assert count == 1
    for token in address_list:
        assert token.text == 'Philadelphia'
    assert expected == result
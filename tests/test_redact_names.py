import redactor as rd
import warnings


def test_redact_names():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    result = '\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588\u2588\u2588 was an American professional basketball player'
    name_list = ['Kobe', 'Bryant']
    temp = []
    text = 'Kobe Bryant was an American professional basketball player'
    expected, names, count = rd.redact_names(text)
    assert count == 2
    for key in names:
        temp.append(key.text)
    assert temp == name_list
    assert len(names) == 2
    assert expected == result
import redactor as rd

def test_unicode_char():
    word = '7 DEC'
    result = '\u2588' + ' ' + '\u2588\u2588\u2588'
    expected = rd.unicode_char(word)
    assert expected == result
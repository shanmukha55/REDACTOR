import redactor as rd

def test_redact_phones():
    text = 'Kobe Bryant phone number is not 405-258-4568'
    result = 'Kobe Bryant phone number is not \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588'
    expected,dates,count = rd.redact_phones(text)
    assert count == 1
    assert dates == ['405-258-4568']
    assert expected == result
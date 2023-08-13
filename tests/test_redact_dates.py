import redactor as rd

def test_redact_dates():
    text = 'Kobe Bryant was born on 23 August 1978'
    result = 'Kobe Bryant was born on \u2588\u2588 \u2588\u2588\u2588\u2588\u2588\u2588 \u2588\u2588\u2588\u2588'
    expected,dates,count = rd.redact_dates(text)
    assert count == 1
    assert dates == ['23 August 1978']
    assert expected == result

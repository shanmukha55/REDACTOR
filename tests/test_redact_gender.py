import redactor as rd
import warnings

def test_redact_gender():
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    text = 'Kobe Bryant was an American professional basketball player. He spent his entire 20-year career with the Los Angeles Lakers in the National Basketball Association (NBA)'
    result = 'Kobe Bryant was an American professional basketball player. \u2588\u2588 spent \u2588\u2588\u2588 entire 20-year career with the Los Angeles Lakers in the National Basketball Association (NBA)'
    expected,gender_list,count = rd.redact_gender(text)
    assert count == 2
    assert gender_list == ['He', 'his']
    assert expected == result
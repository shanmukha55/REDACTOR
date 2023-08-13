

## Project Description
This project redacts sensitive information like names, phone numbers, addresses, etc from text file and writes the redacted data into .redacted file.


## Installation/Getting Started
---
1. Pipenv to create and manage virtual environment for the project.
   > pipenv install
2. Packages required to run this project are in pipfile which will be downloaded in step1.
3. Once, the packages are successfully installed, the project can be executed using
   > pipenv run python redactor.py --input *.txt --names --dates --phones --genders --address --concept 'table' --output 'files' --stats stdout

4. Pytests can be runnable using below command
   > pipenv run python -m pytest

## Packages/Modules
---
- `Spacy` is a python library for Natural Language Processing. It features NER, POS tagging, dependency parsing and more.
    - [en_core_web_sm](https://spacy.io/models/en) is a small English pipeline trained on written web text.
    - [en_core_web_md](https://spacy.io/models/en) is a medium English pipeline trained on written web text.
    - [en_core_web_lg](https://spacy.io/models/en) is a large English pipeline trained on written web text.
- `Glob` is a python module used to return all file paths that match a specific pattern.
- `OS` is a python module that provides functions for interacting with the operating system.
- `pytest` is a framework to write small, readable tests, and can scale to support complex functional testing for applications and libraries.
    - In this project, pytest is used to create [unit tests](#tests) for each functionality
- `Warnings` is a Python module used to show warning messages.
    - In this project, warnings module is used in pytests to ignore deprecationwarnings.
##  Approach to Developing the code
---
1. `get_files(args)`
   This function takes args as a parameter, matches the given pattern with list of files and returns list of matched files.
2. `read_text_file(file_to_read)`
   This function takes a file from a list of files, opens and reads content from a file.
3. `unicode_char(Word)`
   This function takes a redacted string and replaces that string with unicode character(\u2588).
4. `redact_names(text)`
   This function takes file contents in a string and redacts names using spacy.
5. `redact_dates(text)`
   This function takes file contents in a string and redact dates.
6. `redact_phones(text)`
   This function takes file contents in a string and redacts phone numbers.
7. `redact_gender(text)`
   This function takes file contents in a string and redacts gender revealing words.
8. `redact_address(text)`
   This function takes file contents in a string and redacts addresses.
9. `redact_concepts(text, args, temp)`
   This function takes file contents and divide the text into sentences then checking similarity between given concept word/words with each word in a sentence. If the similarity is more than 0.5 then that sentence containing that word is redacted.
    - `Word similarity` is a number between 0 to 1 which tells us how close two words are, semantically.
10. `stats(args, text, file)`
    This function calls every redacted function, redacts every value and writes into a file if a folder is passed in command line or writes into standard output stream if stdout is passed.
11. `write_tostatfile(redacted_terms, count, file, args)`
    This function when called from stats() function writes the stats of redacted values into **.stats** file in a given folder from command line in stats argument.
12. `write_stdout(redacted_terms, count)`
    This function when called from stats() function prints the stats of redacted values into standard output stream.
13. `output(args, complete_data, files)`
    This function takes the complete data after redaction and writes the output in a **.redacted** file  in a given folder from command line in output argument.

## Tests
---
1. **`test_get_files().py`**
   | Function | Test Function | Description  |   
   |   --- |   --- |   ---
   |   `get_files(args)`    |    `test_empty_input()`    |    when input argument is empty,it tests whether the execution terminates.
   |   `get_files(args)`    |    `test_get_files()`    |    when input argument passed, it test whether the matched pattern files are extracted.
2. **`test_unicode.py`**
   | Function | Test Function | Description  |   
   |   --- |   --- |   ---
   |   `unicode_char(Word)`    |    `test_unicode_char()`    |    Tests whether the unicode character is replaced in a given string.

3. **`test_redact_names.py`**
   | Function | Test Function | Description  |   
   |   --- |   --- |   ---
   |   `redact_names(text)`    |    `test_redact_names()`    |    Tests whether the names are redacted correctly from a file.

4. **`test_redact_dates.py`**
   | Function | Test Function | Description  |   
   |   --- |   --- |   ---
   |   `redact_dates(text)`    |    `test_redact_dates()`    |    Tests whether the dates are redacted correctly from a file.

5. **`test_redact_phones().py`**
   | Function | Test Function | Description  |   
   |   --- |   --- |   ---
   |   `redact_phones(text)`    |    `test_redact_phones()`    |    Tests whether the phone numbers are redacted correctly from a file.

6. **`test_redact_gender.py`**
   | Function | Test Function | Description  |   
   |   --- |   --- |   ---
   |   `redact_gender(text)`    |    `test_redact_gender()`    |    Tests whether the gender revealing terms are redacted correctly from a file.
7. **`test_redact_address.py`**
   | Function | Test Function | Description  |   
   |   --- |   --- |   ---
   |   `redact_address(text)`    |    `test_redact_address()`    |    Tests whether the addresses are redacted correctly from a file.
8. **`test_redact_concepts.py`**
   | Function | Test Function | Description  |   
   |   --- |   --- |   ---
   |   `redact_concepts(text, args, temp)`    |    `test_redact_concepts()`    |    Tests whether the conceptual sentences are redacted correctly from a file.
   |   `redact_concepts(text, args, temp)`    |    `test_redact_multiple_concepts()`    |    Tests whether the multiple conceptual sentences are redacted correctly from a file.
9. **`test_stats.py`**
   | Function | Test Function | Description  |   
   |   --- |   --- |   ---
   |   `stats(args, text, file)`    |    `test_stats()`    |    Tests whether all the redacted functions are applied on a given file contents.
10. **`test_write_tostatfile.py`**
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `write_tostatfile(redacted_terms, count, file, args)`    |    `test_write()`    |    Tests whether all the stats are written to a file.
11. **`test_output.py`**
    | Function | Test Function | Description  |   
    |   --- |   --- |   ---
    |   `output(args, complete_data, files)`    |    `test_output()`    |    Tests whether the output(complete file data after redaction) is written to a file.
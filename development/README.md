## Current speed test

    function                        time(x50) fraction
    token_replacement               0.000007  0.000082
    unidecoder                      0.000008  0.000097
    dedash                          0.000340  0.004072
    titlecaps                       0.001735  0.020745
    decaps_text                     0.002472  0.029570
    replace_acronyms                0.006495  0.077685
    identify_parenthetical_phrases  0.006601  0.078951
    separated_parenthesis           0.006701  0.080145
    replace_from_dictionary         0.025758  0.308071
    pos_tokenizer                   0.033493  0.400582

## Development notes

+ Update the version number in `nlpre/_version.py`
+ Draft a release in github
+ Update the new tarbar location in `setup.py`
+ Build the distribution file `python setup.py sdist`

Use the following `~/.pypirc` file (with an updated username and password)

    [distutils]
    index-servers=
        pypi
        test
    
    [test]
    repository=https://test.pypi.org/legacy/
    username=
    password=
    
    [pypi]
    repository = https://upload.pypi.org/legacy/
    username=
    password=

+ Push the release to [pypi test](https://test.pypi.org/project/nlpre/) `twine upload -r test dist/*`
+ Push the release to [pypi live](https://pypi.org/project/nlpre/) `twine upload dist/*`
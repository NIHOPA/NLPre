## Current speed test (spaCy 2.1.0)

```
                                    time      frac
function                                          
unidecoder                      0.000002  0.000005
token_replacement               0.000038  0.000121
dedash                          0.000354  0.001111
replace_from_dictionary         0.000584  0.001831
identify_parenthetical_phrases  0.005599  0.017542
titlecaps                       0.058357  0.182846
pos_tokenizer                   0.058928  0.184635
decaps_text                     0.059976  0.187919
separated_parenthesis           0.064683  0.202667
replace_acronyms                0.070638  0.221324
```

#### pattern.en speed test
 
    function                        time      frac
    unidecoder                      0.000008  0.000122
    token_replacement               0.000008  0.000125
    dedash                          0.000369  0.005811
    replace_from_dictionary         0.000442  0.006967
    titlecaps                       0.001944  0.030632
    decaps_text                     0.002502  0.039425
    identify_parenthetical_phrases  0.005824  0.091770
    replace_acronyms                0.006972  0.109849
    separated_parenthesis           0.007339  0.115635
    pos_tokenizer                   0.038059  0.599663

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
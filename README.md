# Natural Language Preprocessing (NLPre)

[![Build Status](https://travis-ci.org/NIHOPA/NLPre.svg?branch=master)](https://travis-ci.org/NIHOPA/NLPre)
[![codecov](https://codecov.io/gh/NIHOPA/NLPre/branch/master/graph/badge.svg)](https://codecov.io/gh/NIHOPA/NLPre)

Ultimately, this will be a python package to preprocess text.
Part of the [`word2vec-pipeline`](https://github.com/NIHOPA/word2vec_pipeline).
Developed by the [Office of Portfolio Analysis](https://dpcpsi.nih.gov/opa/aboutus) at the [National Institutes of Health](https://www.nih.gov/).

### Installation

    pip install git+git://github.com/NIHOPA/NLPre.git

### Timeline

+ [x] Import modules from pipeline_word2vec
+ [x] Document which functions exists in README
+ [x] Write unit tests for individual functions
+ [x] Write unit tests for pipelines (multi-function)
+ [x] Write doc strings for all functions
+ [x] Format as proper python package
+ [x] Complete import (missing ABBR phrase replacement)
+ [ ] Clean and format the README
+ [ ] Upload to pypy


### What's included?

**dedash**

When text is passed though a word-processor sometimes hyphenations with
with newlines are inserted. This module attempts to correct the hyphenation
pattern by joining words that if they appear in an English word list.

**decaps**

We presume that case is important, but only for complicated words like fMRI.
This module corrects casing by lowering all words with only one capital letter.

`Hello world` -> `hello world`

**remove_parenthesis**

Parentheticals (statements in parenthesis) are removed as long as
they are balanced.

**replace_from_dictionary**

Noun phrases from a predefined dictionary are replaced. The [MeSH](https://www.nlm.nih.gov/mesh/) dictionary comes included.

**replace_phrases**

Phrases found though an abbreviation finder (not included yet), are replaced.

**titlecaps**

WHY ARE SOME SENTENCES IN ALL CAPS? These sentences are converted to lower case.

**token_replacement**

Simple token replacement (% -> `percent`)

**pos_tokenizer**

Parts of speech are filtered out by using a white-list. 

**unidecoder**

Converts Unicode phrases into ASCII equivalent, (`β-sheet` -> `b-sheet`).

**identify_parenthetical_phrases**

`What is Health and Human Services (HHS)?` gets tokenized as `counter[(('Health', 'and', 'Human', 'Services'), 'HHS')]`


# Natural Language Preprocessing (NLPre)

[![Build Status](https://travis-ci.org/NIHOPA/NLPre.svg?branch=master)](https://travis-ci.org/NIHOPA/NLPre)
[![codecov](https://codecov.io/gh/NIHOPA/NLPre/branch/master/graph/badge.svg)](https://codecov.io/gh/NIHOPA/NLPre)
[![PyPI](https://img.shields.io/pypi/v/nlpre.svg)](https://pypi.python.org/pypi/nlpre)


NLPre is a text (pre)-processing library that helps smooth some of the inconsistencies found in real-world data.
Correcting for issues like random capitalization patterns, strange hyphenations, and abbreviations are essential parts of wrangling textual data but are often left to the user.

While this library was developed by the [Office of Portfolio Analysis](https://dpcpsi.nih.gov/opa/aboutus) at the [National Institutes of Health](https://www.nih.gov/) to correct for historical artifacts in our data, we envision this module to encompass a broad spectrum of problems encountered in the preprocessing step of natural language processing.

NLPre is part of the [`word2vec-pipeline`](https://github.com/NIHOPA/word2vec_pipeline).

### Installation

For the latest release, use

    pip install nlpre

For the development version, use

    pip install git+git://github.com/NIHOPA/NLPre.git -U

### Example

```python
from nlpre import titlecaps, dedash, identify_parenthetical_phrases
from nlpre import replace_acronyms, replace_from_dictionary

text = ("LYMPHOMA SURVIVORS IN KOREA. Describe the correlates of unmet needs "
        "among non-Hodgkin lymphoma (NHL) surv- ivors in Korea and identify "
        "NHL patients with an abnormal white blood cell count.")

ABBR = identify_parenthetical_phrases()(text)
parsers = [dedash(), titlecaps(), replace_acronyms(ABBR),
           replace_from_dictionary(prefix="MeSH_")]

for f in parsers:
    text = f(text)

print(text)

''' lymphoma survivors in korea .
    Describe the correlates of unmet needs among non_Hodgkin_lymphoma
    ( non_Hodgkin_lymphoma ) survivors in Korea and identify non_Hodgkin_lymphoma
    patients with an abnormal MeSH_Leukocyte_Count . '''
```

To see a detailed log of the changes made, set the level to `logging.INFO` or `logging.DEBUG`,

```python
import nlpre, logging
nlpre.logger.setLevel(logging.INFO)
```

### What's included?

| Function | Description |
| --- | --- |
| [**replace_from_dictionary**](nlpre/replace_from_dictionary.py) | Replace phrases from an input dictionary. The replacement is done without regard to case, but punctuation is handled correctly. The [MeSH ](https://www.nlm.nih.gov/mesh/) (Medical Subject Headings) dictionary is built-in. <br> `(11-Dimethylethyl)-4-methoxyphenol is great` <br> `MeSH_Butylated_Hydroxyanisole is great` |
| [**replace_acronyms**](nlpre/replace_acronyms.py) | Replaces acronyms and abbreviations found in a document with their corresponding phrase. If an acronym is explicitly identified with a phrase in a document, then  all instances of that acronym in the document will be replaced with the given phrase. If there is no explicit indication what the phrase is within the document, then the most common phrase associated with the acronym in the given counter is used. <br> `The EPA protects trees` <br> `The Environmental_Protection_Agency protects trees`
| [**identify_parenthetical_phrases**](nlpre/identify_parenthetical_phrases.py) | Identify abbreviations of phrases found in a parenthesis. Returns a counter and can be passed directly into [`replace_acronyms`](nlpre/replace_acronyms). <br> `'Environmental Protection Agency (EPA)` <br> `Counter((('Environmental', 'Protection', 'Agency'), 'EPA'):1)` |
| [**separated_parenthesis**](nlpre/separated_parenthesis.py) | Separates parenthetical content into new sentences. This is useful when creating word embeddings, as associations should only be made within the same sentence. Terminal punctuation of a period is added to parenthetical sentences if necessary. <br> `Hello (it is a beautiful day) world.` <br>`Hello world. it is a beautiful day .` |
| [**pos_tokenizer**](nlpre/pos_tokenizer.py) | Removes all words that are of a designated part-of-speech (POS) from a document. For example, when processing medical text, it is useful to remove all words that are not nouns or adjectives. POS detection is provided by the [`pattern.en.parse`](http://www.clips.ua.ac.be/pages/pattern-en#parser) module. <br> `The boy threw the ball into the yard` <br> `boy ball yard` |
| [**unidecoder**](nlpre/unidecoder.py) | Converts Unicode phrases into ASCII equivalent. <br> `α-Helix β-sheet` <br> `a-Helix b-sheet` |
| [**dedash**](nlpre/dedash.py) | Hyphenations are sometimes erroneously inserted when text is passed through a word-processor. This module attempts to correct the hyphenation pattern by joining words that if they appear in an English word list. <br> `How is the treat- ment going` <br> `How is the treatment going` |
| [**decaps_text**](nlpre/decaps_text.py) | We presume that case is important, but only when it differs from title case. This class normalizes capitalization patterns. <br> `James and Sally had a fMRI` <br> `james and sally had a fMRI` |
| [**titlecaps**](nlpre/titlecaps.py) | Documents sometimes have sentences that are entirely in uppercase (commonly found in titles and abstracts of older documents). This parser identifies sentences where every word is uppercase, and returns the document with these sentences converted to lowercase. <br> `ON THE STRUCTURE OF WATER.` <br> `On the structure of water .` |
| [**token_replacement**](nlpre/token_replacement.py) | Simple token replacement. <br> `Observed > 20%` <br> `Observed greater-than 20 percent` |
| [**separate_reference**](nlpre/separate_reference.py) | Separates and optionally removes references that have been concatenated onto words. <br> `Key feature of interleukin-1 in Drosophila3-5 and elegans(7).`<br>`Key feature of interleukin-1 in Drosophila and elegans .` |

### Parallel processing

To run NLPre in parallel, simply create a small pipeline function and pass it to either multiprocessing or [`joblib`](https://github.com/joblib/joblib). For example, continuing from the example from above:

```python
from joblib import Parallel, delayed

def pipeline(x):
    for f in parsers:
        x = f(x)
    return x

docs = [text,]*500
with Parallel(-1) as MP:
    print MP(delayed(pipeline)(x) for x in docs)
```

## License

This project is in the public domain within the United States, and
copyright and related rights in the work worldwide are waived through
the [CC0 1.0 Universal public domain dedication](https://creativecommons.org/publicdomain/zero/1.0/).
# Natural Language Preprocessing (NLPre)

Ultimately, this will be a python package to preprocess text.
Developed by NIH OPA.

### Timeline

+ [x] Import modules from pipeline_word2vec
+ [x] Document which functions exists in README
+ [ ] Write unit tests for individual functions
+ [ ] Write unit tests for pipelines
+ [ ] Write doc strings for all functions
+ [ ] Format as proper python package
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

Parentheicals (statements in parenthesis) are removed as long as
they are balanced.

**replace_from_dict**

Noun phrases from a predefined dictionary are replaced. In this case we have
MeSH already preloaded.

**replace_phrases**

Phrases found though an abbreviation finder (not included yet), are replaced.

**titlecaps**

WHY ARE SOME SENTENCES IN ALL CAPS? These sentences are converted to lower case.

**token_replacement**

Simple token replacement (% -> `percent`)

**pos_tokenizer**

Parts of speech are filtered out by using a white-list. 




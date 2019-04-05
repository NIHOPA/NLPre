import os
import spacy
from spacy.matcher import Matcher

# Hard code the model into NLPre
f_spacey_init = os.path.join(
    os.path.dirname(__file__), "spacy_models", "en_core_web_sm-2.1.0"
)

nlp = spacy.load(f_spacey_init, disable=["ner"])
matcher = Matcher(nlp.vocab)

# Add in the custom rule for joining dashed words as a single entity
# Seee https://spacy.io/usage/linguistic-features#rule-based-matching
pattern = [{"IS_ASCII": True}, {"ORTH": "-"}, {"IS_ASCII": True}]
matcher.add("PRESERVE_DASHES", None, pattern)


def dash_merger(doc):
    # this will be called on the Doc object in the pipeline
    matched_spans = []
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        matched_spans.append(span)

    # Merge into one token after collecting all matches
    for span in matched_spans:
        span.merge()

    return doc


nlp.add_pipe(dash_merger, first=True)  # add it right after the tokenizer

import os
import spacy
from spacy.util import load_model_from_init_py

# Hard code the model into NLPre
f_spacey_init = os.path.join(
    os.path.dirname(__file__), 'spacy_models', 'en_core_web_sm-2.0.0')
nlp = spacy.load(f_spacey_init)

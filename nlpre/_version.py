# One canonical source for the version number,
# Versions should comply with PEP440.

__version__ = "2.1.1"

# 2.1.1 Fixed non-functional Grants preset
# 2.1.0 Add presets: Grants
# 2.0.4 Removed older dependencies (mysqlclient)
# 2.0.3 Add dictionaries to manifest for pypi
# 2.0.2 Fix manifest for pypi
# 2.0.1 Add the spaCy model to the manifest

# 2.0.0 Major update, breaking changes! pattern.en replaced with spaCy.
# + Most spaces before terminal punc removed.
# + Support for python 2 has been dropped
# + Backend NLP engine `pattern.en` has been replaced with `spaCy`
# + Support for custom dictionaries in `replace_from_dictionary`
# + Option for suffix to be used instead of prefix in `replace_from_dictionary`
# + URL replacement can now remove emails
# + `token_replacement` can remove symbols

# 1.2.3 Fixed the version for mysqlclient to help windows installs.
# Version tracking started in 1.2.3 (add to the top)

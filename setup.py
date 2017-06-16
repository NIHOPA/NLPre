import setuptools
import os

__local__ = os.path.abspath(os.path.dirname(__file__))

f_version = os.path.join(__local__, 'nlpre', '_version.py')
exec(open(f_version).read())

# Get the long description from the relevant file
long_description = '''NLPre
=================================
A collection of Natural Language Preprocessing (NLPre) utilities, suitable
for a pipeline.
'''

setuptools.setup(
    name='nlpre',
    packages=setuptools.find_packages(),

    # Include package data...
    include_package_data=True,

    description='Natural Language Preprocessing (NLPre) utilities.',
    long_description=long_description,
    version=__version__,

    # The project's main homepage.
    url="https://github.com/NIHOPA/NLPre",
    download_url='https://github.com/NIHOPA/NLPre/archive/v1.1.0.tar.gz',

    # Author details
    author="Travis Hoppe",
    author_email="travis.hoppe+nlpre@gmail.com",

    # Choose your license
    license='CC0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5  -Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Education',
        'Intended Audience :: Financial and Insurance Industry',

        'Natural Language :: English',
        
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Filters',
        'Topic :: Utilities',
        
        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
    ],

    # What does your project relate to?
    keywords="NLP",

    test_suite='nose.collector',
    tests_require=['nose'],
)

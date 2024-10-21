# cit-parser

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.12+-brightgreen.svg)
<!-- ![PyPI](https://img.shields.io/pypi/v/cit-parser.svg) -->

`cit-parser` is a Python library designed to detect and extract legal citations from blocks of text using the `legal-citation-bert` transformer model. 


## Prerequisites

- **Python**: Version 3.12 or higher.
- **Pydantic v2**

## Installation

Install `cit-parser` via your package manager of choice, e.g., `uv add cit-parser`


**__Download the spaCy Language Model__**

cit-parser relies on spaCy’s en_core_web_sm model for sentence segmentation. You need to download this model after installing the library.

python -m spacy download en_core_web_sm


__Verify the Installation:__
You can verify that the model is installed correctly by running:

python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('spaCy model loaded successfully!')"

If the model is installed correctly, you should see:

spaCy model loaded successfully!


## Usage

Once installed and set up, you can use cit-parser to detect legal citations in your text.

Basic Example

from cit_parser import parse

# Sample text with legal citations
text = "In the landmark case of 410 U.S. 113 (1973), the Supreme Court established..."

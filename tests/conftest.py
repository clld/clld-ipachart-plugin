import pathlib

import pytest
from pyclts import CLTS
from pycldf import Wordlist


@pytest.fixture
def clts():
    return CLTS(pathlib.Path(__file__).parent / 'clts')


@pytest.fixture
def cldf():
    return Wordlist.from_metadata(pathlib.Path(__file__).parent / 'cldf' / 'Wordlist-metadata.json')

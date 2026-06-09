import pathlib

import pytest
from pyclts import CLTS
from pycldf import Wordlist, Database


@pytest.fixture
def clts():
    return CLTS(pathlib.Path(__file__).parent / 'clts')


@pytest.fixture
def cldf():
    return Wordlist.from_metadata(pathlib.Path(__file__).parent / 'cldf' / 'Wordlist-metadata.json')


@pytest.fixture
def cldf_db(cldf, tmp_path):
    db = Database(cldf, fname=tmp_path / 'test.db')
    db.write_from_tg()
    return db

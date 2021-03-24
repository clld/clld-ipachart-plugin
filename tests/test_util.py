import pathlib

from clld.db.models.common import Language

from clld_ipachart_plugin.util import *


def test_clts_from_input(mocker):
    mocker.patch('clld_ipachart_plugin.util.input', lambda *args: None)
    clts1 = clts_from_input(pathlib.Path(__file__).parent.joinpath('clts'))
    assert clts1

    mocker.patch('clld_ipachart_plugin.util.input',
                 lambda *args: pathlib.Path(__file__).parent.joinpath('clts'))
    clts2 = clts_from_input('.')
    assert clts2
    assert clts1.repos == clts2.repos


def test_load_inventories(clts, cldf):
    lang = Language()
    load_inventories(cldf, clts, {'1': lang})
    assert 'a' in dict(lang.jsondata['inventory'])

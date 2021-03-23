from clld.db.models.common import Language

from clld_ipachart_plugin.util import load_inventories


def test_load_inventories(clts, cldf):
    lang = Language()
    load_inventories(cldf, clts, {'1': lang})
    assert 'a' in dict(lang.jsondata['inventory'])

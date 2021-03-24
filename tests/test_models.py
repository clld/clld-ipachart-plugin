from sqlalchemy import Integer, ForeignKey, Column
from clld.db.meta import CustomModelMixin
from clld.db.models.common import Language, Contribution
from pyclts.ipachart import Segment

from clld_ipachart_plugin.models import InventoryMixin
from clld_ipachart_plugin.util import load_inventories


def test_InventoryMixin(clts, cldf):
    class Lang(CustomModelMixin, Language, InventoryMixin):
        pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)

    lang = Lang()
    load_inventories(cldf, clts, {'1': lang})
    ctx = lang.render_inventory()
    assert ctx['uncovered']


def test_InventoryMixin_custom(clts, cldf):
    class Lang2(CustomModelMixin, Contribution, InventoryMixin):
        pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)

        def make_segment(self, sound_bipa, sound_name, request=None, **kw):
            return Segment(
                sound_bipa=sound_bipa,
                sound_name=sound_name,
                href='http://example.com/{}/{}'.format(kw['path'], request))

    lang = Lang2()
    load_inventories(cldf, clts, {'1': lang})
    lang.update_jsondata(
        inventory=[(k, (v, dict(path='x'))) for k, v in lang.jsondata['inventory']])
    ctx = lang.render_inventory(request=5, exclude=[])
    assert 'http://example.com/x/5' in ctx['vowels_html']
    assert '+' in [p.sound_bipa for p in ctx['uncovered']]
    ctx = lang.render_inventory(request=5)
    assert '+' not in [p.sound_bipa for p in ctx['uncovered']]

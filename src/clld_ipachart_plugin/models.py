from collections.abc import Sequence, Iterable
from typing import Any, Optional, Callable

from pyclts.ipachart import Segment, VowelTrapezoid, PulmonicConsonants


def _ensure_str(s):
    return s if isinstance(s, str) else '\n'.join(s)


class Charts:
    def __init__(self, inventory: Iterable[Segment], render_kw: Optional[dict[str, Any]] = None):
        d = VowelTrapezoid()
        self._covered = d.fill_slots(inventory)
        self.vowels_html, self.vowels_css = d.render(**render_kw or {})
        self.vowels_css = _ensure_str(self.vowels_css)
        d = PulmonicConsonants()
        self._covered = self._covered.union(d.fill_slots(inventory))
        self.consonants_html, self.consonants_css = d.render(**render_kw or {})
        self.consonants_css = _ensure_str(self.consonants_css)

    def __contains__(self, item):
        return item in self._covered


class InventoryMixin:
    """
    This mixin expects data about a phoneme inventory to be stored as `list` of pairs
    (BIPA grapheme, val) under the "inventory" key in the objects' `jsondata`, where val is either
    - a CLTS sound name or
    - a pair (sound name, metadata), where metadata is a `dict`.
    """
    def make_segment(self, sound_bipa, sound_name, request=None, **_):
        """
        Inheriting classes should overwrite this method to customize the way segments in the IPA
        charts are rendered.

        :param sound_bipa: BIPA grapheme.
        :param sound_name: CLTS sound name.
        :param request: The current request or `None`.
        :param _: `dict` with additional metadata for the segment.
        :return: A `Segment` instance.
        """
        return Segment(
            sound_bipa=sound_bipa,
            sound_name=sound_name,
            href='https://clts.clld.org/parameters/{}'.format(sound_name.replace(' ', '_')))

    def _make_segment(self, sound_bipa, val, request=None):
        if isinstance(val, (list, tuple)) and len(val) == 2:
            sound_name, data = val
        else:
            sound_name, data = val, {}
        return self.make_segment(sound_bipa, sound_name, request=request, **data)

    def inventory(
            self,
            req,
            customize_segment: Optional[Callable[[Segment], Segment]] = None,
    ) -> list[Segment]:
        """
        Inheriting classes may overwrite this method, if they store "raw" inventory data
        differently.

        :return: `list` of `Segment` instances.
        """
        res = [self._make_segment(k, v, request=req) for k, v in self.jsondata['inventory']]
        if customize_segment:
            return list(map(customize_segment, res))
        return res

    def render_inventory(
            self,
            request=None,
            exclude: Sequence[str] = ('+',),
            customize_segment: Optional[Callable[[Segment], Segment]] = None,
            render_kw: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """
        Usage: In an apps' `util.py` include code like
        ```python
        def language_detail_html(context=None, request=None, **kw):
            return context.render_inventory(request=request)
        ```

        :param request: The current request.
        :param exclude: `list` or `tuple` of graphemes (or pseudo-graphemes) to exclude.
        :param customize_segment: A callable accepting and returning a (possibly modified) \
        `Segment` instance. This can be used for example to add `css_class`.
        :param render_kw: An optional `dict` which is passed to the `render` methods of vowel and \
        consonant chart.
        :return: `dict` suitable for inclusion in template context:
        - "vowels_css": CSS snippet to style the vowels trapezoid.
        - "consonants_css" CSS snippet to style the consonants table.
        - "vowels_html": The IPA vowel trapezoid.
        - "consonants_html": The IPA consonants table.
        - "uncovered": `list` of `Segment` instances which didn't fit into trapezoid or table.
        """
        inventory = self.inventory(request, customize_segment=customize_segment)
        charts = Charts(inventory, render_kw)
        return {
            'vowels_html': charts.vowels_html,
            'vowels_css': charts.vowels_css,
            'consonants_html': charts.consonants_html,
            'consonants_css': charts.consonants_css,
            'uncovered': [
                p for i, p in enumerate(inventory)
                if (i not in charts) and p.sound_bipa not in exclude]
        }

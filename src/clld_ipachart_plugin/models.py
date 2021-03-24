from pyclts.ipachart import Segment, VowelTrapezoid, PulmonicConsonants


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

    def inventory(self, req):
        """
        Inheriting classes may overwrite this method, if they store "raw" inventory data
        differently.

        :return: `list` of `Segment` instances.
        """
        return [self._make_segment(k, v, request=req) for k, v in self.jsondata['inventory']]

    def render_inventory(self, request=None, exclude=('+',)):
        """
        Usage: In an apps' `util.py` include code like
        ```python
        def language_detail_html(context=None, request=None, **kw):
            return context.render_inventory(request=request)
        ```

        :param request: The current request.
        :param exclude: `list` or `tuple` of graphemes (or pseudo-graphemes) to exclude.
        :return: `dict` suitable for inclusion in template context:
        - "vowels_css": CSS snippet to style the vowels trapezoid.
        - "consonants_css" CSS snippet to style the consonants table.
        - "vowels_html": The IPA vowel trapezoid.
        - "consonants_html": The IPA consonants table.
        - "uncovered": `list` of `Segment` instances which didn't fit into trapezoid or table.
        """
        inventory = self.inventory(request)
        res = {}
        d = VowelTrapezoid()
        covered = d.fill_slots(inventory)
        res['vowels_html'], res['vowels_css'] = d.render()
        d = PulmonicConsonants()
        covered = covered.union(d.fill_slots(inventory))
        res['consonants_html'], res['consonants_css'] = d.render()
        res['uncovered'] = [
            p for i, p in enumerate(inventory)
            if (i not in covered) and p.sound_bipa not in exclude]
        return res

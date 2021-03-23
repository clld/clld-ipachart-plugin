import collections

__all__ = ['load_inventories']


def load_inventories(cldf, clts, languages):
    """
    Compute phoneme inventories from segments in a Wordlist and assign them to jsondata of Language
    objects.

    :param cldf: `pycldf.Wordlist` instance.
    :param clts:  `pyclts.CLTS` instance.
    :param languages: `dict` mapping language IDs to `clld.db.models.common.Language` instances.
    """
    inventories = collections.defaultdict(set)
    for form in cldf.iter_rows(
            'FormTable', 'id', 'form', 'languageReference', 'parameterReference'):
        inventories[form['languageReference']] = inventories[form['languageReference']].union(
            form['Segments'])

    for lid, inv in inventories.items():
        inv = [clts.bipa[c] for c in inv]
        languages[lid].update_jsondata(
            inventory=[(str(c), c.name) for c in inv if hasattr(c, 'name')])

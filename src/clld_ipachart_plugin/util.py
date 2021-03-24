import pathlib
import collections

from pyclts import CLTS

__all__ = ['load_inventories', 'clts_from_input']


def clts_from_input(default_path):
    """
    Get a CLTS instance for a path specified by the user.

    :param default_path: Path to use in case of empty user input.
    :return: `CLTS` instance.
    """
    default_path = pathlib.Path(default_path)
    res = input('Path to clone of cldf-clts/clts [{}]: '.format(str(default_path)))
    return CLTS(pathlib.Path(res) if res else default_path)


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
            'FormTable', 'id', 'form', 'languageReference', 'parameterReference', 'segments'):
        inventories[form['languageReference']] = inventories[form['languageReference']].union(
            form['segments'])

    for lid, inv in inventories.items():
        inv = [clts.bipa[c] for c in inv]
        languages[lid].update_jsondata(
            inventory=[(str(c), c.name) for c in inv if hasattr(c, 'name')])

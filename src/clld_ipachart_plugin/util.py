import pathlib
import collections
from typing import Union

from pyclts import CLTS
from pyclts.models import Marker
from pycldf import Dataset, Database
from clld.db.models.common import Language

__all__ = ['load_inventories', 'clts_from_input']


def clts_from_input(default_path: Union[str, pathlib.Path]) -> CLTS:
    """
    Get a CLTS instance for a path specified by the user.

    :param default_path: Path to use in case of empty user input.
    :return: `CLTS` instance.
    """
    default_path = pathlib.Path(default_path)
    res = input('Path to clone of cldf-clts/clts [{}]: '.format(str(default_path)))
    return CLTS(pathlib.Path(res) if res else default_path)


def load_inventories(cldf: Union[Dataset, Database], clts: CLTS, languages: dict[str, Language]):
    """
    Compute phoneme inventories from segments in a Wordlist and assign them to jsondata of Language
    objects.

    :param cldf: `pycldf.Wordlist` instance.
    :param clts:  `pyclts.CLTS` instance.
    :param languages: `dict` mapping language IDs to `clld.db.models.common.Language` instances.
    """
    inventories = collections.defaultdict(collections.Counter)
    if isinstance(cldf, Dataset):
        for form in cldf.iter_rows(
                'FormTable', 'id', 'form', 'languageReference', 'parameterReference', 'segments'):
            inventories[form['languageReference']].update(form['segments'])
    else:
        assert isinstance(cldf, Database)
        for form in cldf.query("select cldf_languageReference, cldf_segments from FormTable"):
            inventories[form[0]].update(form[1].split())

    for lid, inv in inventories.items():
        inv = [(clts.bipa[c], freq) for c, freq in inv.most_common()]
        inv = [(s, freq) for s, freq in inv if not isinstance(s, Marker)]
        languages[lid].update_jsondata(
            frequencies={str(c): freq for c, freq in inv if hasattr(c, 'name')},
            inventory=[(str(c), c.name) for c, _ in inv if hasattr(c, 'name')])

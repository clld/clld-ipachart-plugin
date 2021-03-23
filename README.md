# clld-ipachart-plugin

[![Build Status](https://github.com/clld/clld-ipachart-plugin/workflows/tests/badge.svg)](https://github.com/clld/clld-ipachart-plugin/actions?query=workflow%3Atests)
[![PyPI](https://img.shields.io/pypi/v/clld-ipachart-plugin.svg)](https://pypi.org/project/clld-ipachart-plugin)

A plugin for the [`clld`](https://pypi.org/project/clld) package.


## Usage

`clld-ipachart-plugin` provides
- A model mixin [`clld_audio_plugin.models.InventoryMixin`](src/clld_ipachart_plugin/models.py)
  providing functionality to render IPA chart components.
- A utility function [`clld_ipachart_plugin.util.load_inventories`](src/clld_ipachart_plugin/util.py)
  to load inventory data from segmented forms of a CLDF Wordlist.
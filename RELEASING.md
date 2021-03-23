Releasing clld-ipachart-plugin
==============================

- Do platform test via tox (making sure statement coverage is at 100%):
```
tox -r
```

- Change setup.py version to the new version number.

- Bump version number:
```
git commit -a -m"<VERSION>"
```

- Create a release tag:
```
git tag -a v<VERSION> -m"release <VERSION>"
```

- Release to PyPI:
```
python setup.py clean --all
rm dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```

- Push to github:
```
git push origin
git push --tags
```

- Append `.dev0` to the version number in `setup.py` for the new development cycle.

- Commit/push the version change:
```shell
git commit -a -m "bump version for development"
git push origin
```

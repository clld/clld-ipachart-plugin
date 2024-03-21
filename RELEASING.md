Releasing clld-ipachart-plugin
==============================

- PEP8
  ```shell
  flake8 src
  ```

- Do platform test via tox (making sure statement coverage is at 100%):
  ```shell
  tox -r
  ```

- Change setup.cfg version to the new version number.

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
  python -m build -n
  twine upload dist/*
  ```

- Push to github:
  ```shell
  git push origin
  git push --tags
  ```

- Append `.dev0` to the version number in `setup.cfg` for the new development cycle.

- Commit/push the version change:
  ```shell
  git commit -a -m "bump version for development"
  git push origin
  ```

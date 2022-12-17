# Contributing

Contributions are very welcome: every one helps, and credit will always be given.

There are many ways in which to contribute, all of them are appreciated:

## Types of Contributions

### Report bugs

Report bugs by [opening an issue][gh-issues] on GitHub. If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whoever wants to fix it.

### Implement features

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whoever wants to implement it.
Before working on a new feature, please [start a discussion][gh-discussions] to propose the feature to ensure it aligns with the project goals.

### Write documentation

The project can always use more documentation, whether as part of the official docs, added via docstrings, or even on the web in blog posts, articles, and such.

### Submit feature requests

You can [submit a feature request][gh-issues] by opening an issue on GitHub. When proposing a new feature:

- Explain in detail how it would work.
- Keep the scope as narrow as possible, to make it easier to implement.
- Remember that this is a volunteer-driven project, and that contributions are welcome 😊

## Get started

Ready to contribute? Here's how to set yourself up for local development.

1. Fork the repo on GitHub.

2. Clone your fork locally:

   ```shell
   $ git clone git@github.com:your_name_here/aiosoma.git
   Cloning into 'aiosoma'...
   ```

3. Install the project dependencies with [Poetry](https://python-poetry.org):

   ```shell
   $ poetry install
   Creating virtualenv aiosoma ...
   ...
   ```

4. Create a branch for local development:

   ```shell
   $ git checkout -b name-of-your-bugfix-or-feature
   Switched to a new branch 'name-of-your-bugfix-or-feature'
   ```

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass our tests:

   ```shell
   $ poetry run pytest
   =============================== test session starts ==================================================
   platform linux -- Python 3.9.14, pytest-7.2.0, pluggy-1.0.0 -- /path/to/your/aiosoma/.venv/bin/python
   ...
   ```

6. Linting is done through [pre-commit](https://pre-commit.com). Provided you have the tool installed globally, you can run them all as one-off:

   ```shell
   $ poetry run pre-commit run -a
    debug statements (python)................................................Passed
    check builtin type constructor use.......................................Passed
    check for case conflicts.................................................Passed
    check docstring is first.................................................Passed
    check json...............................................................Passed
    check toml...............................................................Passed
    check xml................................................................Passed
    check yaml...............................................................Passed
    detect private key.......................................................Passed
    fix end of files.........................................................Passed
    trim trailing whitespace.................................................Passed
    poetry-check.............................................................Passed
    prettier.................................................................Passed
    pyupgrade................................................................Passed
    isort....................................................................Passed
    black....................................................................Passed
    codespell................................................................Passed
    flake8...................................................................Passed
    mypy.....................................................................Passed
    bandit...................................................................Passed
   ```

   Or better, install the hooks once and have them run automatically each time you commit:

   ```shell
   $ poetry run pre-commit install
   pre-commit installed at .git/hooks/pre-commit
   ```

7. Commit your changes and push your branch to GitHub:

   ```shell
   $ git add .
   $ git commit -m "feat(something): your detailed description of your changes"
   $ git push origin name-of-your-bugfix-or-feature
    Enumerating objects: 24, done.
    Counting objects: 100% (24/24), done.
    Delta compression using up to 24 threads
    Compressing objects: 100% (12/12), done.
    Writing objects: 100% (14/14), 6.98 KiB | 6.98 MiB/s, done.
    Total 14 (delta 5), reused 0 (delta 0), pack-reused 0
    remote: Resolving deltas: 100% (5/5), completed with 5 local objects.
    To github.com:your-name-here/aiosoma.git
    + xxxxxxx...xxxxxxx name-of-your-bugfix-or-feature -> name-of-your-bugfix-or-feature
   ```

   Note: your commit message must adhere to [the conventional commits](https://www.conventionalcommits.org) standard. GitHub Actions [lint both the source code and the commit message](https://github.com/Djelibeybi/aiosoma/actions/workflows/ci.yml) during the CI process. If you installed the `pre-commit` hooks in the previous step, the message will be checked when you commit.

8. Submit a pull request through the GitHub website or using the GitHub CLI (if you have it installed):

   ```shell
   $ gh pr create --fill
   ...follow the prompts...
   ```

## Pull request guidelines

We like to have pull requests open as soon as possible. They are a great place to discuss any piece of work, even unfinished. You can create a draft pull request for any work in progress. Here are a few guidelines to follow:

1. Include tests for feature or bug fixes.
2. Update the documentation for significant features.
3. Ensure tests are passing on CI.

## Tips

To run a subset of tests:

```shell
$ poetry run pytest tests/<test_file.py>::<test_name>
tests/test_file.py::test_name PASSED
```

## Releasing a new version

The release of new versions of `aiosoma` are automated and that automation is controlled by the Semantic Release workflow. The next version number is derived from [the commit logs](https://python-semantic-release.readthedocs.io/en/latest/commit-log-parsing.html#commit-log-parsing) by [python-semantic-release](https://python-semantic-release.readthedocs.io/en/latest/index.html). The [`CHANGELOG`][gh-changelog] is automatically updated as well.

[gh-issues]: https://github.com/Djelibeybi/aiosoma/issues
[gh-discussions]: https://github.com/Djelibeybi/aiosoma/discussions
[gh-changelog]: https://github.com/Djelibeybi/aiosoma/blob/main/CHANGELOG.md

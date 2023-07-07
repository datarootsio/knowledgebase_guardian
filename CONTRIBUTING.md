# Contributing

We are always looking for contributions! Below you can find some relevant information and standards for `KnowledgeBase Guardian`.

## Setup ⚙️

After cloning the [repo](https://github.com/datarootsio/knowledgebase_guardian/), make sure to set up
the environment.

### Poetry 📜

We use [Poetry](https://python-poetry.org/) for both managing environments and packaging.
That means you need to install poetry but from there you can use the tool to create the
environment.

```bash
pip install poetry==1.5.1
poetry install  # installs dependencies
```

#### Usage

Remember that to use the environment you can use the `poetry run <COMMAND>` command or
initialize the shell with `poetry shell`. For example, if you want to detect contradictions you could run

```bash
poetry run python src/detect_contradictions.py
```

or alternatively

```bash
poetry shell
python src/detect_contradictions.py
```

## Development 🛠

We welcome new features, bugfixes or enhancements. There are a
few standards we adhere to, that are required for new features.

### Mypy

We use type hints! Not only that, they are enforced and checked (with
[Mypy](https://mypy.readthedocs.io/en/stable/index.html)). There are a couple of reasons for using type hints, mainly:

1. Better code coverage (avoid errors during runtime)
2. Improved code understanding

If you are not familiar with type hints and Mypy, a good starting point is watching the
[Type-checked Python in the real world - PyCon 2018](https://www.youtube.com/watch?v=pMgmKJyWKn8)
talk.

### Linting

In regards to code quality, we use a couple of linting tools to maintain the same "style"
and uphold to the same standards. For that, we use:

1. [Black](https://black.readthedocs.io/en/stable/) for code formatting
2. [isort](https://pycqa.github.io/isort/) for imports
3. [Flake8](https://pycqa.github.io/isort/) for style enforcement

### Pre-commit

[`Pre-commit`](https://pre-commit.com/) is the tool that automates everything, eases the
workflow and run checks in CI/CD. It's highly recommended installing `pre-commit` and the
hooks during development.

## Tests 🗳

Currently the code is not tested, but this will change in the future. Therefore, we ask you to include unit tests to ensure that everything works as expected.

We'll use
[`pytest`](https://docs.pytest.org/en/6.2.x/) for testing and
[`Pytest-cov`](https://pytest-cov.readthedocs.io/en/latest/) for checking how much of
the code is covered in our tests.

The tests should mimic the package directory structure.

## Contributors 👨‍💻👩‍💻

`KnowledgeBase Guardian` was created by [Senne Batsleer](https://github.com/SenneDataroots) and buils on previous work at Dataroots by [Andrea Benevenuta](https://github.com/andreabenevenut), [Virginie Marelli](https://github.com/virginiemar), [Tim Leers](https://github.com/tleers), [Hans Tierens](https://github.com/HansTierens) and [Jan Yperman](https://github.com/jandataroots). It is currently
maintained by [dataroots](https://github.com/datarootsio).

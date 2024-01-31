## Getting Started

To run this code, you'll need to have Python 3.9, 3.10, 3.11, or 3.12 installed on your machine. You'll also need to
install the required packages by running the following commands from inside the project folder:

```shell
python3 -m venv venv
```
```shell
source venv/bin/activate
```
```shell
python3 -m pip install .[dev]
```
```shell
pre-commit install
```

## Code Submissions

### Style

If your text editor doesn't support [.editorconfig](https://editorconfig.org/), please reference the [.editorconfig file](.editorconfig) for some basic formatting norms.
Regardless, `ruff format .` should be run to standardize formatting before attempting to commit.

### Tests

Pytest is used to simplify testing and avoid committing broken code. Before committing, please run `pytest` in the project folder and resolve any errors.

[![PyPI Version](https://img.shields.io/pypi/v/sruthi)](https://pypi.org/project/sruthi/)
[![Tests + Linting Python](https://github.com/metaodi/sruthi/actions/workflows/lint_python.yml/badge.svg)](https://github.com/metaodi/sruthi/actions/workflows/lint_python.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# srupymarc



The `srupymarc` package is a fork of the [`sruthi`](https://github.com/metaodi/sruthi/tree/master) package, which is a client for python to make [SRU requests (Search/Retrieve via URL)](http://www.loc.gov/standards/sru/). `Srupymarc` extends the original sruthi package by adding one additional field to the `searchRetrieve` operation to allow users to choose between the following output formats:
- Flattened dict (as implemented in the original sruthi package)
- [Pymarc](https://pymarc.readthedocs.io/en/latest/) record (default)

The functionality of the `explain` operation remains unchanged.

Currently only **SRU 1.1 and 1.2** is supported.

## Table of Contents

* [Installation](#installation)
* [Usage](#usage)
* [Testing](#testing)

## Installation

Install this package via the wheels included in the `dist/` directory:

```
$ cd dist
$ pip install srupymarc-2.0.0-py3-none-any.whl
```
## Usage

The `explain` operation can be performed as follows:

```python
info = srupymarc.explain(url)
```

The `searchRetrieve` operation can be performed as follows:

```python
records = srupymarc.searchretrieve(url, query, record_schema, sru_version="1.2", maximum_records=10, output_format="pymarc", suppress_leader_warning=True)
```
The `pymarc` output format is only valid with the `marcxml` record schema. Attempting to use an alternative record schema will yield a runtime error. The `flatten` output format, however, is schema-agnostic.
## Example script

The `alma_queries_sruthi.py` script provides examples of how to use this package with the Alma SRU API. To run this example, first ensure you are connected to the VPN, so you can access the Alma API. Then, create a python venv as follows:
```bash
python -m venv sru_venv
cd examples
pip install -r requirements.txt
```

Use the ```alma_queries_sruthi.py``` script in the `examples` directory as follows:

```python alma_queries_sruthi.py -o [OPERATION] -q [QUERY]```

For example, here is how you can query all the articles that include the term `pothos` in the title. This is a recommended query to test with as it produces just enough records to observe sruthi's record iterating behaviors as described below.

```python alma_queries_sruthi.py -o searchRetrieve -q query3```

Note that when you request data through `sruthi`, it will first request the number of records specified by the `maximum_records` parameter. If you iterate through the returned records, then it will continuously make new API calls to request subsequent records until all the matches have been exhausted. Be wary of this if your query matches a large number of records.

You can update the output format specification by modifying the `alma_sru_config.toml` file. Valid output format designations are "flatten" for flattened dictionaries, and "pymarc" for pymarc records.

## Suppressing the leader warning

The `suppress_leader_warning` parameter is set to `True` by default. 
If you are using `pymarc` as your output format, and one of the records you pull contains a `leader` field of a length other than 24, then `srupymarc` will automatically replace the leader field with a default leader so that pymarc can parse the record. 
If you would like to see this warning, set the `suppress_leader_warning` parameter to `False`.

## Testing

To run the unit tests, first create a virtual environment and install the packages needed for testing.

```bash
python -m venv testing_venv
pip install -r test-requirements.txt
pip install dist/srupymarc-2.0.0-py3-none-any.whl
```

Then, move to the `tests` directory and run the tests:

```bash
cd tests
python -m pytest
```

## Build distribution files

If you have created code updates and would like to include the updates in the distribution files, first make sure the code passes all the tests, and then run the following from the root of this repository:
This will create the `.whl` and `.tar.gz` distribution files in the `dist/` directory.
```bash
pip install build
python -m build
```

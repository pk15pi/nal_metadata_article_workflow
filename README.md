# nal_metadata_article_workflow
This Python library supports the metadata work in the Django article workflow found at
https://github.com/USDA-REE-ARS/nal_django_article_workflow

## Splitter

This module supports the splitting of metadata collection documents into single record documents while preserving the 
metadata original schema or DTD.

## Mapper

This module supports mapping single metadata record documents into the same format.

## Citation

This module supports a Citation object to hold record information in a standardized format. 
The mapper function from the mapper module maps input record strings to Citation objects.
The citation module includes the overarching Citation, as well as the following objects for subfield information: License, Author, Funder, and Local.
The Local field is used for fields that do not map directly into the CrossRef JSON format.

## Importation

The `mapper` and `splitter` functions, and the necessary classes from the `citation` module can be imported locally as follows.

First, create and activate a virtual environment.

```commandline
python -m venv mapper_splitter_venv
source mapper_splitter_venv/bin/activate
```

Next, install the `metadata_routines` module in your virtual environment. This command must be run from the root directory of this repository since pip will look for the `metadata_routines` package in the current directory.
```commandline
pip install --editable ./metadata_routines
```
Finally, import the `mapper()` and `splitter()` functions from their respective modules. Launch python and import the functions as follows.
```python
from mapper import mapper
from splitter import splitter
from citation import *
```
Now the functions `mapper()` and `splitter()` are accessible. You can confirm that they are accessible by running these functions in the python console.
```python
mapper()
splitter()
```
When we run these functions with no arguments, we expect to get a `TypeError` indicating that we are missing positional arguments. This tells us that we have imported our functions correctly.

Next, we can confirm that the `Citation` object from the citation module has been imported correctly by creating an empty Citation object in the python console:

```python
Citation()
```
The console will print out a Citation object with empty fields.

You can uninstall the `metadata_routines` package as follows.
```bash
pip uninstall metadata_routines
```
## Testing
To run the `pytest` tests, first ensure that the `mapper_splitter_venv` environment is still active. If not, follow the instructions under [Importation](#importation) to create the virtual environment and install the packages.

Next, install `pytest` and the `pytest-datadir` plugin.

```bash
pip install pytest
pip install pytest-datadir
```
Now we can test our code. When you run the `pytest` command, `pytest` will run all tests in the current directory or in any subdirectories. So, we can run the `pytest` command from the `tests/` directory to run all the tests in both `tests/mapper_test/` and `tests/splitter_test/`, or we can run the `pytest` command in either subdirectory to run just the tests for the mapper or splitter code respectively. 

Test both mapper and splitter code:
```bash
cd tests
pytest
```

Test just mapper code:
```bash
cd tests/mapper_test
pytest
```

Test just splitter code:
```bash
cd tests/splitter_test
pytest
```

Alternatively, we can use the `--ignore` option to tell pytest to ignore a subdirectory. Here's another way we could run just the mapper tests:
```bash
cd tests
pytest --ignore=splitter_test
```

##### Warning!
While you can run the `pytest` command from the root directory of this repository, that would cause `pytest` to try to run the tests within the `srupymarc` repository. These tests will fail when the `pytest` command is run from the root directory. If you wish to run `pytest` from the root of this repo, use the `--ignore` option to tell `pytest` not to run the tests within `srupymarc`.

## Updating code

Since we installed `metadata_routines` to our virtual environment with the `--editable` option, when we change our source code, those changes will be reflected in our virtual environment. Thus, we can update our source code and immediately run tests on our source code without having to build wheels and reinstall `metadata_routines` to our enviornment. 

## Updating Distribution

To incorporate new updates into the distribution files, run the following commands:

```bash
cd metadata_routines
pip install build
python -m build
```

This will build both the .whl and .tar.gz distribution files and store them in the `metadata_routines/dist/` directory.

## Installing from wheels

You may wish to install the `metadata_routines` package from wheels instead of from the local source code. Once you have built your wheels in the `metadata_routines/dist/` directory, you can install from wheels. You can also use this method if you wish to use the `metadata_routines` package in a different repository by just downloading/copying over the wheel file instead of the entire repository.

First, ensure that you don't currently have a local version of `metadata_routines` installed. You can uninstall as follows:
```bash
pip uninstall metadata_routines
```
Next, install the `metadata_routines` package by pointing to the location of the .whl file.
```bash
cd metadata_routines/dist
pip install metadata_routines-0.0.0-py3-none-any.whl
```
You can confirm that the package installation worked as expected by attempting to import the mapper() and splitter() functions:
```python
from mapper import mapper
mapper()
from splitter import splitter 
splitter()
```
If you have updated the wheels and would like to update your virtual environment to use the new version of the .whl file, run the following from whichever directory has the updated .whl file:

```bash
pip install --force-reinstall metadata_routines-0.0.0-py3-none-any.whl
```
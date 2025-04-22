# nal_metadata_article_workflow
This Python library supports the metadata work in the Django article workflow found at
https://github.com/USDA-REE-ARS/nal_django_article_workflow

## Splitter

This module supports the splitting of metadata collection documents into single record documents while preserving the 
metadata original schema or DTD.

## Mapper

This module supports mapping single metadata record documents into the same format.

## Citation

This module provides a Citation object to hold record information in a standardized format. 
The mapper function from the mapper module maps input record strings to Citation objects.
The citation module includes the overarching Citation, as well as the following objects for subfield information: License, Author, Funder, and Local.
The Local field is used for fields that do not map directly into the CrossRef JSON format.

## type_and_match

This module is responsible for determining the type of a citation object based on its title, and matching it against existing records. This module connects to the PubAg SOLR index and Alma to find records with matching DOIs or MMSIDs.

#### Note: The `type_and_match` function in this module requires connection to the VPN (if running locally), and requires the `SOLR_SERVER` environment variable to be set to the PubAg SOLR server URL.

## metadata_quality_review

The `metadata_quality_review` subpackage provides functions to review and validate the quality of metadata in citation records. It includes checks for various fields such as volume, issue, page, title, author, primary author, issue date, and abstract. The subpackage ensures that the metadata meets certain quality standards and provides feedback through cataloguer notes.

## Importation
The `mapper` and `splitter` functions, the necessary classes from the `citation` module, and the `ArticleTyperMatcher` class can be imported locally as follows.

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
from type_and_match.type_and_match import ArticleTyperMatcher
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

Finally, we can confirm that the `ArticleTyperMatcher` class from the `type_and_match` module has been imported correctly by creating an instance of the class in the python console:

```python
ArticleTyperMatcher()
```

You can uninstall the `metadata_routines` package as follows.
```bash
pip uninstall metadata_routines
```
## Testing
To run the `pytest` tests, first ensure that the `mapper_splitter_venv` environment is still active. If not, follow the instructions under [Importation](#importation) to create the virtual environment and install the packages.

Now we can test our code. When you run the `pytest` command, `pytest` will run all tests in the current directory or in any subdirectories. So, we can run the `pytest` command from the `tests/` directory to run all the tests in subdirectories of `tests/`. Alternatively, we can run the `pytest` command in a subdirectory to run just the tests for that respective module. 

Test code in all modules:
```bash
cd tests
pytest
```

Test just one module, e.g., the mapper module:
```bash
cd tests/mapper_test
pytest
```

Alternatively, we can use the `--ignore` option to tell pytest to ignore a subdirectory. Here's another way we could all tests except for the `splitter` tests:
```bash
cd tests
pytest --ignore=splitter_test
```

## Updating code

Since we installed `metadata_routines` to our virtual environment with the `--editable` option, when we change our source code, those changes will be reflected in our virtual environment. Thus, we can update our source code and immediately run tests on our source code without having to build wheels and reinstall `metadata_routines` to our environment. 

## Updating Distribution

To incorporate new updates into the distribution files, run the following commands:

```bash
cd metadata_routines
pip install build
python -m build
```

This will build both the .whl and .tar.gz distribution files and store them in the `metadata_routines/dist/` directory.

## GitHub Actions

When a PR is created, a github action will lint the code with flake8, build the distribution files, and test the code in the `tests/` directory with pytest.

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

## Srupymarc Submodule

`nal_srupymarc` is a separate package and GitHub module created to handle SRU requests in python. A Git submodule is a repository embedded inside another Git repository. It allows you to keep a Git repository as a subdirectory of another Git repository. This can be useful for including and managing dependencies or libraries that are developed separately.

Note: The `nal_srupymarc` repository contains the `srupymarc` package. Thus, we use pip to install `nal_srupymarc`, and once installed, we import `srupymarc`. The `nal_srupymarc` repository is a submodule of the `nal_metadata_article_workflow` repository. The `srupymarc` package is used by the `mapper` and `splitter` functions in the `metadata_routines` package. The `nal_srupymarc` submodule must be initialized by following the instructions below in order to locally install the `srupymarc` package needed by the `metadata_routines` package.

### Managing the `nal_srupymarc` Submodule

The `nal_srupymarc` submodule must be initialized so we can populate the directory with the contents of the `nal_srupymarc` repository. You can either initialize the submodule when you first clone the repository or after cloning it.

#### Initialize `nal_srupymarc` when first cloning the repository:

If you are cloning `nal_metadata_article_workflow` for the first time, use the `--recurse-submodules` flag to clone the repository and initialize the `nal_srupymarc` submodule in one step:
```bash
git clone --recurse-submodules https://github.com/USDA-REE-ARS/nal_metadata_article_workflow
```

...or with ssh:

```bash
git clone --recurse-submodules git@github.com:USDA-REE-ARS/nal_metadata_article_workflow.git
```

#### Initialize `nal_srupymarc` after cloning the repository:
If you have just cloned `nal_metadata_article_workflow` and need to initialize the `nal_srupymarc` submodule, run the following command from the root of this repository:
   
```bash
git submodule init
git submodule update
```

#### Updating `nal_srupymarc`:

To update `nal_srupymarc` to the latest commit from its remote repository, navigate to the `nal_srupymarc` directory and pull the latest changes:
    ```bash
    cd nal_srupymarc
    git pull origin main
    ```


By following these steps, you can effectively manage the `nal_srupymarc` submodule within this project.
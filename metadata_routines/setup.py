from setuptools import setup

setup(
    name="metadata_routines",
    packages=['mapper', 'splitter', 'citation',
              'metadata_quality_review', 'type_and_match',
              'pid_minter', 'citation_to_marc'],
    url='https://github.com/USDA-REE-ARS/nal_metadata_article_workflow',
    license='Government Purpose Rights',
    author='Chuck Schoppet',
    author_email='chuck.schoppet@usda.gov',
    description='Metadata libraries for NAL article citation workflow',
    install_requires=["lxml", "mysql", "pymarc", "requests", "wheel", "pyyaml",
                      "tomli", "python-dateutil", "pysolr", "langdetect"],
    package_data={'': ['*.toml']},
    include_package_data=True
)

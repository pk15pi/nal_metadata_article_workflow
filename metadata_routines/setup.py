from setuptools import setup

setup(
    name="metadata_routines",
    packages=['mapper', 'splitter', 'citation',
              'metadata_quality_review', 'type_and_match',
              'pid_minter', 'citation_to_marc', 'annotate_subject_terms',
              'article_staging', 'handle_minter', 'alma_s3'],
    url='https://github.com/USDA-REE-ARS/nal_metadata_article_workflow',
    license='Government Purpose Rights',
    author='Chuck Schoppet',
    author_email='chuck.schoppet@usda.gov',
    description='Metadata libraries for NAL article citation workflow',
    install_requires=["lxml", "mysql", "pymarc", "requests", "wheel", "pyyaml",
                      "tomli", "python-dateutil", "pysolr", "langdetect",
                      "python-doi"],
    package_data={'': ['*.toml']},
    include_package_data=True
)

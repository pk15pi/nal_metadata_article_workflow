from setuptools import setup

setup(
    name="metadata_routines",
    packages=['mapper', 'splitter', 'citation'],
    url='https://github.com/USDA-REE-ARS/nal_metadata_article_workflow',
    license='Government Purpose Rights',
    author='Chuck Schoppet',
    author_email='chuck.schoppet@usda.gov',
    description='Metadata libraries for NAL article citation workflow',
    install_requires=["lxml"]
)

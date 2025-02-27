# -*- coding: utf-8 -*-

from codecs import open
from setuptools import setup, find_packages
import re

with open('srupymarc/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

with open('README.md', 'r', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='srupymarc',
    packages=find_packages(),
    version=version,
    install_requires=['requests', 'defusedxml', 'xmltodict', 'flatten-dict', 'pymarc'],
    description='SRU client for Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Noa Mills',
    author_email='noa.mills@usda.gov',
    maintainer='Noa Mills',
    maintainer_email='noa.mills@usda.gov',
    url='https://github.com/NoaMillsUSDA-ARS/sruthi',
    download_url='https://github.com/metaodi/sruthi/archive/v%s.zip' % version,
    keywords=['sru', 'search', 'retrieve', 'archive', 'library', 'marc', 'pymarc'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7'
)

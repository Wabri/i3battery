import io
import os

from pathlib import Path
from setuptools import setup, find_packages

NAME = 'i3battery'
DESCRIPTION = 'A lightweight and simple battery notifier and warning for linux'
URL = 'github.com/wabri/i3battery'
EMAIL = 'gabriele.puliti@gmail.com'
AUTHOR = 'Gabriele Puliti'
REQUIRE_PYTHON = '>=3.4.0'

def list_reqs(fname='requirements.txt'):
    with open(fname) as fd:
        return fd.read().splitlines()

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / 'packages' / NAME
print(PACKAGE_DIR)
about = {}

with open(PACKAGE_DIR/'VERSION') as f:
    _version = f.read().strip()
    about['__version__'] = _version

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRE_PYTHON,
    url=URL,
    packages=find_packages(),
    package_data={'i3battery': ['VERSION']},
    install_requires=list_reqs(),
    include_package_data=True
)


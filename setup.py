from setuptools import setup, find_packages

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent
REQUIREMENTS = (HERE / "requirements.txt").read_text().splitlines()

# The text of the README file
README = (HERE / "README.rst").read_text()

setup(
    name="pydsol-model",
    version="0.1",
    description=open("README.rst").read(),
    author="Isabelle M. van Schilt",
    url="https://github.com/imvs95/pydsol-model",
    packages=["pydsol", "pydsol.model"],
    package_dir={'pydsol': 'src/pydsol', "pydsol.model": "src/pydsol/model"},
    install_requires=REQUIREMENTS
)

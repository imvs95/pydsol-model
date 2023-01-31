from setuptools import setup, find_packages

import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent
REQUIREMENTS = (HERE / "requirements.txt").read_text().splitlines()

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name="pydsol-model",
    version="1.0",
    description=open("README.md").read(),
    author="Isabelle M. van Schilt",
    url="https://github.com/imvs95/pydsol-model",
    packages=["pydsol"],
    package_dir={{'pydsol': 'src/pydsol'}},
    install_requires=REQUIREMENTS
)
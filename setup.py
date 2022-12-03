"""Setup for mkaudiocdrimg"""
from platform import system, machine
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mkaudiocdrimg",
    version="1.0",
    author="Pellegrino Prevete",
    author_email="pellegrinoprevete@gmail.com",
    description="Make an audio CD-R image from media files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/tallero/mkaudiocdrimg",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['mkaudiocdrimg = mkaudiocdrimg:main']
    },
    install_requires=[
        'appdirs',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Operating System :: Unix",
    ],
)

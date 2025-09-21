#!/usr/bin/env python
"""Setup for mkaudiocdrimg"""

# SPDX-License-Identifier: GPL-3.0-or-later

#    ----------------------------------------------------------------------
#    Copyright © 2022, 2023, 2024, 2025  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from platform import system, machine
from setuptools import setup, find_packages

with open(
       "README.md",
       "r") as fh:
  long_description = fh.read()

_setup_kwargs = {
  "name":
    "mkaudiocdrimg",
  "version":
    "1.0",
  "author":
    "Pellegrino Prevete",
  "author_email":
    "pellegrinoprevete@gmail.com",
  "description":
    "Make an audio CD-R image from media files",
  "long_description":
    long_description,
  "long_description_content_type":
    "text/markdown",
  "url":
    "https://gitlab.com/tallero/mkaudiocdrimg",
  "packages":
    find_packages(),
  "entry_points": {
    'console_scripts': [
      'mkaudiocdrimg = mkaudiocdrimg.mkaudiocdrimg:_main'] },
  "install_requires": [
      'appdirs',],
  "classifiers": [
    "Programming Language :: Python :: 3",
    ("License :: OSI Approved :: "
     "GNU Affero General Public "
     "License v3 or later (AGPLv3+)"),
    "Operating System :: Unix",
  ]
}
setup(
  **_setup_kwargs)

..
   SPDX-License-Identifier: AGPL-3.0-or-later

   ----------------------------------------------------------------------
   Copyright © 2024, 2025  Pellegrino Prevete

   All rights reserved
   ----------------------------------------------------------------------

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU Affero General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU Affero General Public License for more details.

   You should have received a copy of the GNU Affero General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.


=================
mkaudiocdrimg
=================

--------------------------------------------------------------
Produces an audio CD-R image from media files
--------------------------------------------------------------
:Version: mkaudiocdrimg |version|
:Manual section: 1

Synopsis
========

mkaudiocdrimg *[options]* *[media-source]*

Description
===========

Python program and module which produces
an audio CD-R image from media files using
ffmpeg and shntool.


Positional arguments
=======================

media_source              Media file or a directory containing
                          media files.


Options
=======

--image-name image_name    Output image name.
--out-dir out_dir          Output directory.


Application options
=====================

--tmp-dir tmp_dir          Temporary work directory.
--help                     Display help.

Bugs
====

https://github.com/themartiancompany/mkaudiocdrimg/-/issues

Copyright
=========

Copyright Pellegrino Prevete. AGPL-3.0.

See also
========

* ffmpeg
* shntool

.. include:: variables.rst

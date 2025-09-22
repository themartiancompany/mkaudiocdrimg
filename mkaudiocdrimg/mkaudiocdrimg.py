#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make an audio CD-R image from media files."""

#
#    mkaudiocdrimg.py
#
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
#

from appdirs import *
from argparse import ArgumentParser
import mimetypes as _mimetypes
from os import getcwd, rename
from os import makedirs as _makedirs
from os import umask as _umask
from os import walk as _path_walk
from os.path import basename as _basename
from os.path import abspath as _abspath
from os.path import exists as _path_exists
from os.path import isdir as _path_is_dir
from os.path import join as _path_join
from pathlib import Path
import subprocess as _subprocess
from subprocess import run as _sh
from shutil import which

_app_details = (
  "mkaudiocdrimg",
  "Pellegrino Prevete"
)
dirs = {
  'data':
    user_data_dir(
      *_app_details),
  'config':
    user_config_dir(
      *_app_details),
  'cache':
    user_cache_dir(
      *_app_details)
}

def _discover_media_source(
      *sources):
  _media = set()
  _mimetypes.init()
  for _src in sources:
    _src = _abspath(
             _src)
    if not _path_exists(
             _src):
      print(
        f"Resource at '{_src}' not found, quitting...")
      quit()
    if _path_is_dir(
         _src):
      for _dir, _dirs, _files in _path_walk(
                                   _src):
        for _file in _files:
          _filename = _path_join(
                        _src,
                        _dir,
                        _file) 
          if _is_media(
               _filename):
            _media.add(
              _filename)
    else:
      if _is_media(
           _src):
        _media.add(
          _src)
  return _media

def _is_media(
      _filename):
  _mimestart = _mimetypes.guess_type(
                 _filename)[
                   0]
  if _mimestart != None:
    _mimestart = _mimestart.split(
                  '/')[
                    0]
    if _mimestart in ['audio',
                     'video']:
      return True

def _set_tmpdir(
      _tmp_dir=dirs[
                'cache']):
  _original_umask = _umask(
                     0)
  _path = _path_join(
           _tmp_dir,
           "convert")
  try:
    _makedirs(
      _path,
      0o700,
      exist_ok=True)
  except OSError:
    pass
  _umask(
    _original_umask)

def _preprocess_media(
      *_media,
      _tmp_dir=dirs[
                 'cache']):
  _media_out = set()
  _set_tmpdir(
    _tmp_dir)
  for _m in _media:
    if not _m.endswith(
             '.flac'):
      print(
        f"Converting '{_m}'.")
      _out = _path_join(
               _tmp_dir,
               "convert",
               Path(
                 _basename(
                   _m)).with_suffix(
                '.flac'))
      _pp_cmd = [
        "ffmpeg",
          "-y",
          "-i",
            _m,
          "-c:a",
            "flac",
          "-ar",
            "44100",
          "-sample_fmt",
            "s16",
          _out]
      _sh(
        _pp_cmd,
        stdout=_subprocess.DEVNULL,
        stderr=_subprocess.STDOUT)
      _media_out.add(
        _out)
    else:
      _media_out.add(
        _m)
  return list(
           _media_out)

def _cue_fix_bin_imgname(
      image):
  imgname = _basename(
              image)
  with open(
         f"{image}.cue",
         "r") as handle:
    text = handle.read()
  with open(
         f"{image}.cue",
         "w") as handle:
    handle.write(
      text.replace(
        "joined.wav",
        f"{imgname}.bin"))

def _process_media(
      *_media,
      _out_dir=getcwd(),
      _image_name="out",
      _tmp_dir=dirs[
                'cache'],
      _verbose=False):
  _default_image = _path_join(
                     _out_dir,
                     "joined.wav")
  _image = _path_join(
             _out_dir,
             _image_name)
  if _verbose:
    print(
      f"[mkaudiocdrimg] INFO: Playing '{_media}'")
  _media = _preprocess_media(
             *_media,
             _tmp_dir=_tmp_dir)
  _cue_cmd = [
    "shntool",
    "cue"]
  _cue_cmd.extend(
    _media)
  if _verbose:
    print(
      f"[mkaudiocdrimg] INFO: Running {_cue_cmd}")
  with open(
         f"{_image}.cue",
         "w") as _handle:
    _sh(
      _cue_cmd,
      stdout=_handle)
  _cue_fix_bin_imgname(
    _image)
  _bin_cmd = [
    "shntool",
    "join",
      "-O",
        "always", 
      "-d",
      _out_dir
  ]
  _bin_cmd.extend(
    _media)
  if len(
       _media) == 1:
    _gen_cmd = [
      "shntool",
      "gen",
        "-l",
          "3:00",
        "-O",
          "always",
        "-d",
          dirs[
            'cache']]
    _silence_path = _path_join(
                      dirs[
                        'cache'],
                      "silence.wav")
    _sh(
      _gen_cmd)
    _bin_cmd.append(
      _silence_path)
    _sh(
      _bin_cmd)
  rename(
    _default_image,
    f"{_image}.bin")
  return f"{_image}.bin", f"{_image}.cue"

def _check_requirements():
  if not which(
           "shntool"):
    print(
      ("This program needs 'shntool' "
       "to work. Please install it."))
    exit()

def _mkimg(
      *_media_src,
      _out_dir=getcwd(),
      _image_name="joined",
      _verbose=False):
  if _verbose:
    print(
      "[mkaudiocdrimg] INFO: Making '{_media_src}' into a CDR image.")
  _media = _discover_media_source(
             *_media_src)
  _img_bin, _img_cue = _process_media(
                         *_media,
                         _out_dir=_out_dir,
                         _image_name=_image_name,
                         _verbose=_verbose)
  return _img_bin, _img_cue

def _main():
  _check_requirements()
  _parser_args = {
    "description":
      "Produces an audio CD-R image from media files."
  }
  _parser = ArgumentParser(
              **_parser_args)
  _media_source = {
    'args': [
      'media_source'],
    'kwargs': {
      'nargs':
        '+',
      'action':
        'store',
      'help':
        ("media source; "
         "default: current directory")
    }
  }
  _out_dir = {
    'args': [
      '--out-dir'],
    'kwargs': {
      'dest':
        'out_dir',
      'action':
        'store',
      'default':
        getcwd(),
    'help':
      ("output directory; "
       "default: current")
    }
  }
  _image_name = {
    'args': [
      '--image-name'],
    'kwargs': {
      'dest':
        'image_name',
      'action':
        'store',
      'default':
        'joined',
      'help':
        ("name of the resulting image; "
         "default: joined")
    }
  }
  _tmp_dir = {
    'args': [
      '--tmp-dir'],
    'kwargs': {
      'dest':
        'tmp_dir',
      'action':
        'store',
      'default':
        dirs[
          'cache'],
      'help':
        ("output directory; "
         "default: user")
    }
  }
  _verbose = {
    'args': [
      '--verbose'],
    'kwargs': {
      'dest':
        'verbose',
      'action':
        'store_true',
      'default':
        False,
      'help':
        ("verbose output; "
         "default: False")
    }
  }
  _parser.add_argument(
    *_media_source[
      'args'],
    **_media_source[
      'kwargs'])
  _parser.add_argument(
    *_out_dir[
      'args'],
    **_out_dir[
      'kwargs'])
  _parser.add_argument(
    *_image_name[
      'args'],
    **_image_name[
      'kwargs'])
  _parser.add_argument(
    *_tmp_dir[
      'args'],
    **_tmp_dir[
      'kwargs'])
  _parser.add_argument(
    *_verbose[
      'args'],
    **_verbose[
      'kwargs'])
  _args = _parser.parse_args()
  _mkimg(
    *_args.media_source,
    _out_dir=_args.out_dir,
    _image_name=_args.image_name,
    _verbose=_args.verbose)

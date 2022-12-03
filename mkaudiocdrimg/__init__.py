#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make an audio CD-R image from media files."""

#    mkaudiocdrimg
#
#    ----------------------------------------------------------------------
#    Copyright © 2022  Pellegrino Prevete
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
import mimetypes
from os import getcwd, makedirs, rename, umask, walk
from os.path import abspath, basename, exists, isdir
from os.path import join as path_join
from pathlib import Path
import subprocess
from subprocess import run as sh
from shutil import which

app_details = ("mkaudiocdrimg", "Pellegrino Prevete")
dirs = {'data': user_data_dir(*app_details),
        'config': user_config_dir(*app_details),
        'cache': user_cache_dir(*app_details)}

def discover_media_source(*sources):
    media = set()
    mimetypes.init()
    for src in sources:
        src = abspath(src)
        if not exists(src):
            print(f"Resource at {src} not found, quitting...")
            quit()
        if isdir(src):
            for _dir, _dirs, _files in walk(src):
                for file in _files:
                    filename = path_join(src, _dir, file) 
                    if is_media(filename):
                        media.add(filename)
        else:
            if is_media(src):
                media.add(src)
    return media

def is_media(filename):
    mimestart = mimetypes.guess_type(filename)[0]
    if mimestart != None:
        mimestart = mimestart.split('/')[0]
        if mimestart in ['audio', 'video']:
            return True

def set_tmpdir(tmp_dir=dirs['cache']):
    original_umask = umask(0)
    path = path_join(tmp_dir, "convert")
    try:
        makedirs(path, 0o700, exist_ok=True)
    except OSError:
        pass
    umask(original_umask)

def preprocess_media(*media,
                     tmp_dir=dirs['cache']):
    media_out = set()
    set_tmpdir(tmp_dir)
    for m in media:
        if not m.endswith('.flac'):
            print(f"converting {m}")
            out = path_join(tmp_dir,
                            "convert",
                            Path(basename(m)).with_suffix('.flac'))
            pp_cmd = ["ffmpeg", "-y",
                                "-i", m,
                                "-c:a", "flac",
                                "-ar", "44100",
                                "-sample_fmt", "s16",
                                out]
            sh(pp_cmd,
               stdout=subprocess.DEVNULL,
               stderr=subprocess.STDOUT)
            media_out.add(out)
        else:
            media_out.add(m)
    return list(media_out)

def cue_fix_bin_imgname(image):
    imgname = basename(image)
    with open(f"{image}.cue", "r") as handle:
        text = handle.read()
    with open(f"{image}.cue", "w") as handle:
        handle.write(text.replace("joined.wav",
                                  f"{imgname}.bin"))

def process_media(*media,
                  out_dir=getcwd(),
                  image_name="out",
                  tmp_dir=dirs['cache']):
    default_image = path_join(out_dir, "joined.wav")
    image = path_join(out_dir, image_name)
    media = preprocess_media(*media,
                             tmp_dir=tmp_dir)
    cue_cmd = ["shntool", "cue"]
    cue_cmd.extend(media)
    with open(f"{image}.cue", "w") as handle:
        sh(cue_cmd, stdout=handle)
    cue_fix_bin_imgname(image)
    if len(media) > 1:
        bin_cmd = ["shntool", "join", "-O", "always", 
                                      "-d", out_dir]
        bin_cmd.extend(media)
        sh(bin_cmd)
        rename(default_image, f"{image}.bin")
    elif len(media) == 1:
        rename(media[0], f"{image}.bin")
    return f"{image}.bin", f"{image}.cue"

def check_requirements():
    if not which("shntool"):
        print("This program needs 'shntool' to work. Please install it.")
        exit()

def mkimg(*media_src,
          out_dir=getcwd(),
          image_name="joined"):
    media = discover_media_source(*media_src)
    img_bin, img_cue = process_media(*media,
                                     out_dir=out_dir,
                                     image_name=image_name)
    return img_bin, img_cue

def main():
    check_requirements()
    parser_args = {"description": "Make an audio CD-R image from media files."}
    parser = ArgumentParser(**parser_args)

    media_source = {'args': ['media_source'],
                    'kwargs': {'nargs': '+',
                               'action': 'store',
                               'help': ("media source; "
                                        "default: current directory")}}

    out_dir = {'args': ['--out-dir'],
               'kwargs': {'dest': 'out_dir',
                          'action': 'store',
                          'default': getcwd(),
                          'help': ("output directory; "
                                   "default: current")}}

    image_name = {'args': ['--image-name'],
                  'kwargs': {'dest': 'image_name',
                            'action': 'store',
                            'default': 'joined',
                            'help': ("name of the resulting image; "
                                     "default: joined")}}

    tmp_dir = {'args': ['--tmp-dir'],
               'kwargs': {'dest': 'tmp_dir',
                          'action': 'store',
                          'default': dirs['cache'],
                          'help': ("output directory; "
                                   "default: user")}}

    parser.add_argument(*media_source['args'],
                        **media_source['kwargs'])
    parser.add_argument(*out_dir['args'],
                        **out_dir['kwargs'])
    parser.add_argument(*image_name['args'],
                        **image_name['kwargs'])
    parser.add_argument(*tmp_dir['args'],
                        **tmp_dir['kwargs'])

    args = parser.parse_args()

    mkimg(*args.media_source,
          out_dir=args.out_dir,
          image_name=args.image_name)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
#
# Copyright (C) 2023  Laserlicht
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os

from lodextract.lodextract import unpack_lod
from lodextract.defextract import extract_def
from lodextract.makedef import makedef

DIRECTORY_IN = r"D:\Programme\Heroes of Might and Magic III\Data"
DIRECTORY_OUT = r"R:"
IN_FILTER_SPRITE = [ 'H3ab_spr.lod', 'H3sprite.lod' ] # AB data at the beginning -> H3 overwrite of already existing AB data
IN_FILTER_BITMAP = [ 'H3ab_bmp.lod', 'H3bitmap.lod' ] # AB data at the beginning -> H3 overwrite of already existing AB data

def main():
   for filename in IN_FILTER_SPRITE:
        full_name = os.path.join(DIRECTORY_IN, filename)
        extract_lod(full_name, 'sprite')
   for filename in IN_FILTER_BITMAP:
        full_name = os.path.join(DIRECTORY_IN, filename)
        extract_lod(full_name, 'bitmap')

def extract_lod(file, type):
    if not os.path.exists(os.path.join(DIRECTORY_OUT, 'sd_extract', type)): os.makedirs(os.path.join(DIRECTORY_OUT, 'sd_extract', type), exist_ok=True)
    unpack_lod(file, os.path.join(DIRECTORY_OUT, 'sd_extract', type))
    for root, _, files in os.walk(os.path.join(DIRECTORY_OUT, 'sd_extract', type)):
        for file in files:
            if file.lower().endswith('.def'):
                extract_def(os.path.join(root, file), root)
            if not file.lower().endswith('.png') and not file.lower().endswith('.json'):
                os.remove(os.path.join(root, file))

if __name__ == '__main__':
    main()
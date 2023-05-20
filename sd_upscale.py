#!/usr/bin/env python3
#
# MIT License
# 
# Copyright (c) 2023 Laserlicht
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import multiprocessing
import ffmpeg

DIRECTORY_IN_OUT = r"R:"

SINGLE_CORE = False
CORES = 24

def main():
    if SINGLE_CORE:
        for f in list(os.walk(os.path.join(DIRECTORY_IN_OUT, 'sd_extract'))):
            upscaletask(f)
    else: #multi core
        pool = multiprocessing.Pool(CORES)
        for result in pool.map(upscaletask, list(os.walk(os.path.join(DIRECTORY_IN_OUT, 'sd_extract')))):
            pass

def upscaletask(f):
    root, _, files = f
    for file in files:
        if file.lower().endswith('.png'):
            stream = ffmpeg.input(os.path.join(root, file), pix_fmt='rgba')
            stream = ffmpeg.filter(stream, 'xbr', n=4)
            if ".dir" in root.lower():
                stream_alpha = ffmpeg.input(os.path.join(root, file), pix_fmt='rgba')
                stream_alpha = ffmpeg.filter(stream_alpha, 'alphaextract')
                stream_alpha = ffmpeg.filter(stream_alpha, 'xbr', n=4)
                stream = ffmpeg.filter([stream, stream_alpha], 'alphamerge')
            stream = ffmpeg.output(stream, os.path.join(root, file + '.tmp.png'), pix_fmt='rgba')
            ffmpeg.run(stream)
            os.remove(os.path.join(root, file))
            os.rename(os.path.join(root, file + '.tmp.png'), os.path.join(root, file))

if __name__ == '__main__':
    main()
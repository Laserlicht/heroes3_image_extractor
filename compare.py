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
from PIL import Image
import base64
from io import BytesIO

from mappinglist import mapping

DIRECTORY_IN = r"R:"
DIRECTORY_OUT = r"R:"

def main():
    sd_bmp = ['.'.join(x.split('.')[:-1]) for x in os.listdir(os.path.join(DIRECTORY_IN, 'sd_mod', 'data')) if x.lower().endswith('.png') and os.path.isfile(os.path.join(DIRECTORY_IN, 'sd_mod', 'data', x))]
    hd_bmp = ['.'.join(x.split('.')[:-1]) for x in os.listdir(os.path.join(DIRECTORY_IN, 'hd_mod', 'data')) if x.lower().endswith('.png') and os.path.isfile(os.path.join(DIRECTORY_IN, 'sd_mod', 'data', x))]

    sd_sprite = ['.'.join(x.split('.')[:-1]) for x in os.listdir(os.path.join(DIRECTORY_IN, 'sd_mod', 'sprites')) if x.lower().endswith('.json') and os.path.isfile(os.path.join(DIRECTORY_IN, 'sd_mod', 'sprites', x))]
    hd_sprite = ['.'.join(x.split('.')[:-1]) for x in os.listdir(os.path.join(DIRECTORY_IN, 'hd_mod', 'sprites')) if x.lower().endswith('.json') and os.path.isfile(os.path.join(DIRECTORY_IN, 'hd_mod', 'sprites', x))]

    sd_sprites = {x:['.'.join(y.split('.')[:-1]) for y in os.listdir(os.path.join(DIRECTORY_IN, 'sd_mod', 'sprites', x + '.dir')) if y.lower().endswith('.png') and os.path.isfile(os.path.join(DIRECTORY_IN, 'sd_mod', 'sprites', x + '.dir', y))] for x in sd_sprite}
    hd_sprites = {x:['.'.join(y.split('.')[:-1]) for y in os.listdir(os.path.join(DIRECTORY_IN, 'hd_mod', 'sprites', x + '.dir')) if y.lower().endswith('.png') and os.path.isfile(os.path.join(DIRECTORY_IN, 'hd_mod', 'sprites', x + '.dir', y))] for x in hd_sprite}

    bmp = list(dict.fromkeys(sd_bmp + hd_bmp))
    sprite = list(dict.fromkeys(sd_sprite + hd_sprite))
    bmp.sort()
    sprite.sort()

    html = "<html><body>"
    html += "<h1>Bitmap</h1>"
    html += '<table style="border:1px solid black;border-collapse:collapse;"><tr><th style="border:1px solid black;">Name</th><th style="border:1px solid black;">Name (HD)</th><th style="border:1px solid black;">SD (complete)</th><th style="border:1px solid black;">HD</th></tr>'
    for item in bmp:
        item_images = {}
        for t in ['sd', 'hd']:
            item_images[t] = ''
            if os.path.isfile(os.path.join(DIRECTORY_IN, t + '_mod', 'data', item + '.png')):
                img = Image.open(os.path.join(DIRECTORY_IN, t + '_mod', 'data', item + '.png'))
                buffered = BytesIO()
                img.thumbnail((48, 48), Image.Resampling.BILINEAR)
                img.save(buffered, format="PNG")
                img_b64 = base64.b64encode(buffered.getvalue()).decode()
                item_images[t] += '<img src="data:image/png;base64,' + img_b64 + '" title="' + item + '" />'
        html += '<tr><td style="border:1px solid black;">' + item + '</td><td style="border:1px solid black;">' + ('' if item not in mapping() else mapping()[item]) + '</td><td style="border:1px solid black;">' + item_images['sd'] + '</td><td style="border:1px solid black;">' + item_images['hd'] + "</td></tr>"
    html += "</table>"
    html += "<h1>Sprite</h1>"
    html += '<table style="border:1px solid black;border-collapse:collapse;"><tr><th style="border:1px solid black;">Name</th><th style="border:1px solid black;">Name (HD)</th><th style="border:1px solid black;">SD (complete)</th><th style="border:1px solid black;">HD</th></tr>'
    for item in sprite:
        item_images = {}
        for t in ['sd', 'hd']:
            item_images[t] = ''
            if os.path.isdir(os.path.join(DIRECTORY_IN, t + '_mod', 'sprites', item + '.dir')):
                for image in os.listdir(os.path.join(DIRECTORY_IN, t + '_mod', 'sprites', item + '.dir')):
                    if os.path.isfile(os.path.join(DIRECTORY_IN, t + '_mod', 'sprites', item + '.dir', image)):
                        img = Image.open(os.path.join(DIRECTORY_IN, t + '_mod', 'sprites', item + '.dir', image))
                        buffered = BytesIO()
                        img.thumbnail((24, 24), Image.Resampling.BILINEAR)
                        img.save(buffered, format="PNG")
                        img_b64 = base64.b64encode(buffered.getvalue()).decode()
                        item_images[t] += '<img src="data:image/png;base64,' + img_b64 + '" title="' + image + '" />'
        html += '<tr><td style="border:1px solid black;">' + item + '</td><td style="border:1px solid black;">' + ('' if item not in mapping() else mapping()[item]) + '</td><td style="border:1px solid black;">' + item_images['sd'] + '</td><td style="border:1px solid black;">' + item_images['hd'] + "</td></tr>"
    html += "</table>"
    html += "</html></body>"

    with open(os.path.join(DIRECTORY_OUT, "compare.html"), "w") as f:
        f.write(html)

if __name__ == '__main__':
    main()
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
import shutil
import json

DIRECTORY_IN = r"R:"
DIRECTORY_OUT = r"R:"

def main():
    basedir_in = os.path.join(DIRECTORY_IN, 'hd_extract')
    basedir_out  = os.path.join(DIRECTORY_OUT, 'hd_mod')

    if not os.path.exists(basedir_out): os.makedirs(basedir_out, exist_ok=True)
    if not os.path.exists(os.path.join(basedir_out, 'data')): os.makedirs(os.path.join(basedir_out, 'data'), exist_ok=True)
    if not os.path.exists(os.path.join(basedir_out, 'sprites')): os.makedirs(os.path.join(basedir_out, 'sprites'), exist_ok=True)

    with open(os.path.join(basedir_out, "mod.json"), "w") as f:
        f.write('''
{	
	"name" : "HD textures (official)",
	"description" : "HD textures (official)",
	"version" : "1.0.0",
	"author" : "",
	"contact" : "",
	"modType" : "Other",
	"compatibility" :
	{
		"min" : "1.2.0"
	},
	"changelog" : 
	{ 
		"1.0.0" : [ "Initial" ]
	}
}
        '''.strip())

    for root, _, files in os.walk(basedir_in):
        for file in files:
            if 'bitmap_' in root.lower():
                shutil.copyfile(os.path.join(root, file), os.path.join(basedir_out, 'data', file.lower()))
            if 'sprite_' in root.lower():
                base = os.path.basename(os.path.normpath(root))
                if not os.path.exists(os.path.join(basedir_out, 'sprites', base.lower() + '.dir')): os.makedirs(os.path.join(basedir_out, 'sprites', base.lower() + '.dir'), exist_ok=True)
                shutil.copyfile(os.path.join(root, file), os.path.join(basedir_out, 'sprites', base.lower() + '.dir', file.lower()))

    for item in os.listdir(os.path.join(basedir_out, 'sprites')):
        if not os.path.isfile(os.path.join(basedir_out, 'sprites', item)):
            data = {}
            data['sequences'] = []
            data['sequences'].append({
                'group': 0,
                'frames': [item + '/' + x for x in os.listdir(os.path.join(basedir_out, 'sprites', item)) if x.lower().endswith('.png') and os.path.isfile(os.path.join(basedir_out, 'sprites', item, x))],
                'type': 0,
                'format': 0
            })
            with open(os.path.join(basedir_out, 'sprites', item.replace('.dir', '.json')), 'w') as f:
                json.dump(data, f, indent=4)

if __name__ == '__main__':
    main()
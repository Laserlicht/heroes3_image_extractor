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

DIRECTORY_IN = r"R:"
DIRECTORY_OUT = r"R:"

def main():
    basedir_in = os.path.join(DIRECTORY_IN, 'sd_extract')
    basedir_out  = os.path.join(DIRECTORY_OUT, 'sd_mod')

    if not os.path.exists(basedir_out): os.makedirs(basedir_out, exist_ok=True)

    with open(os.path.join(basedir_out, "mod.json"), "w") as f:
        f.write('''
{	
	"name" : "Upscaled SD textures",
	"description" : "Upscaled SD textures",
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

    shutil.copytree(os.path.join(basedir_in, 'bitmap'), os.path.join(basedir_out, 'data')) 
    shutil.copytree(os.path.join(basedir_in, 'sprite'), os.path.join(basedir_out, 'sprites')) 

if __name__ == '__main__':
    main()
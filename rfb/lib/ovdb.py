# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2018 Pixar
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# ##### END MIT LICENSE BLOCK #####

#
# Python Imports
#
import os

#
# Blender Imports
#
import bpy

#
# RenderManForBlender Imports
#


# locate_openVDB_cache
def locate_cache(frameNum):
    if not bpy.data.is_saved:
        return None

    # filename (without extension)
    fnm = os.path.splitext(os.path.split(bpy.data.filepath)[1])[0]

    # cache directory
    cdr = os.path.join(bpy.path.abspath("//"), 'blendcache_%s' % fnm)

    if not os.path.exists(cdr):
        return None

    for f in os.listdir(os.path.join(bpy.path.abspath("//"), cdr)):
        if '.vdb' in f and "%06d" % frameNum in f:
            return os.path.join(bpy.path.abspath("//"), cdr, f)

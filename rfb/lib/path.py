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

# <pep8-80 compliant>

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
from . import tmpl


def user_path(path,
              scene=None,
              obj=None,
              display_driver=None,
              layer_name=None,
              pass_name=None):
    #
    # first env vars, in case they contain special blender variables
    # recursively expand these (max 10), in case there are vars in vars
    #
    # Mmh, this is unix only, what about %name% under Windows?
    #
    for i in range(10):
        path = os.path.expandvars(path)
        if '$' not in path:
            break

    unsaved = True if not bpy.data.filepath else False
    #
    # first builtin special blender variable
    #
    if unsaved:
        path = path.replace('{blend}', 'untitled')
    else:
        name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        path = path.replace('{blend}', name)

    if scene is not None:
        path = path.replace('{scene}', scene.name)

    if display_driver is not None:
        if display_driver == "tiff":
            path = path.replace('{file_type}', display_driver[-4:])
        else:
            path = path.replace('{file_type}', display_driver[-3:])

    if obj is not None:
        path = path.replace('{object}', obj.name)

    if layer_name is not None:
        path = path.replace('{layer}', layer_name)

    if pass_name is not None:
        path = path.replace('{pass}', pass_name)

    #
    # convert ### to frame number
    #
    if scene is not None:
        path = tmpl.hashnum(path, scene.frame_current)

    # convert blender style // to absolute path
    if unsaved:
        path = bpy.path.abspath(path, start=bpy.app.tempdir)
    else:
        path = bpy.path.abspath(path)

    return path


def expand(path, scene=None, obj=None, display_driver=None,
           layer_name=None, pass_name=None):
    #
    # first env vars, in case they contain special blender variables
    # recursively expand these (max 10), in case there are vars in vars
    #
    # Mmh, this is unix only, what about %name% under Windows?
    #
    for i in range(10):
        path = os.path.expandvars(path)
        if '$' not in path:
            break

    unsaved = True if not bpy.data.filepath else False
    #
    # first builtin special blender variable
    #
    if unsaved:
        path = path.replace('{blend}', 'untitled')
    else:
        name = os.path.splitext(os.path.basename(bpy.data.filepath))[0]
        path = path.replace('{blend}', name)

    if scene is not None:
        path = path.replace('{scene}', scene.name)

    if display_driver is not None:
        if display_driver == "tiff":
            path = path.replace('{file_type}', display_driver[-4:])
        else:
            path = path.replace('{file_type}', display_driver[-3:])

    if obj is not None:
        path = path.replace('{object}', obj.name)

    if layer_name is not None:
        path = path.replace('{layer}', layer_name)

    if pass_name is not None:
        path = path.replace('{pass}', pass_name)

    #
    # convert ### to frame number
    #
    if scene is not None:
        path = tmpl.hashnum(path, scene.frame_current)

    # convert blender style // to absolute path
    if unsaved:
        path = bpy.path.abspath(path, start=bpy.app.tempdir)
    else:
        path = bpy.path.abspath(path)

    return path


def flist(_p_):
    return [f for f in os.listdir(_p_)]

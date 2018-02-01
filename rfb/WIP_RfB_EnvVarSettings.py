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
import platform

#
# Blender Imports
#
import bpy
from bpy.props import StringProperty

#
# RenderManForBlender Imports
#


class RfB_EnvVarSettings(bpy.types.PropertyGroup):
    if platform.system() == "Windows":
        temp = os.environ.get('TEMP')
        out = StringProperty(
            name="OUT (Output Root)",
            description="Default RIB export path root",
            subtype='DIR_PATH',
            default=os.path.join(temp, 'rfb', '{blend}'))

    else:
        out = StringProperty(
            name="OUT (Output Root)",
            description="Default RIB export path root",
            subtype='DIR_PATH',
            default='/tmp/rfb/{blend}')

    shd = StringProperty(
        name="SHD (Shadow Maps)",
        description="SHD environment variable",
        subtype='DIR_PATH',
        default=os.path.join('$OUT', 'shadowmaps'))

    ptc = StringProperty(
        name="PTC (Point Clouds)",
        description="PTC environment variable",
        subtype='DIR_PATH',
        default=os.path.join('$OUT', 'pointclouds'))

    arc = StringProperty(
        name="ARC (Archives)",
        description="ARC environment variable",
        subtype='DIR_PATH',
        default=os.path.join('$OUT', 'archives'))

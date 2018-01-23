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

#
# Blender Imports
#
from bpy.types import NodeSocketColor
from bpy.props import FloatVectorProperty
from bpy.props import StringProperty

#
# RenderManForBlender Imports
#
from . RM_Socket import RM_Socket
from . RM_NodeSocketColorInterface import RM_NodeSocketColorInterface
from . util import update_func
from .. import rfb


class RM_NodeSocketColor(NodeSocketColor, RM_Socket):
    """RenderMan input/output color socket."""
    bl_idname = 'RendermanNodeSocketColor'
    bl_label = 'RenderMan Color Socket'

    default_value = FloatVectorProperty(
        size=3,
        subtype="COLOR",
        update=update_func
    )
    renderman_type = StringProperty(default='color')

    def draw_color(self, context, node):
        return rfb.reg.get('RGB')

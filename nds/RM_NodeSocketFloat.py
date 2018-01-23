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
# Blender Imports
#
from bpy.types import NodeSocketFloat
from bpy.props import FloatProperty
from bpy.props import StringProperty

#
# RenderManForBlender Imports
#
from . RM_Socket import RM_Socket
from . RM_NodeSocketFloatInterface import RM_NodeSocketFloatInterface
from . import update_func
from .. import rfb


# socket types (need this just for the ui_open)
class RM_NodeSocketFloat(NodeSocketFloat, RM_Socket):
    """RenderMan input/output float socket."""
    bl_idname = 'RendermanNodeSocketFloat'
    bl_label = 'RenderMan Float Socket'

    default_value = FloatProperty(update=update_func)
    renderman_type = StringProperty(default='float')

    def draw_color(self, context, node):
        return rfb.reg.get('FLOAT')

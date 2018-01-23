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
from bpy.types import NodeSocketInt
from bpy.props import IntProperty
from bpy.props import StringProperty

#
# RenderManForBlender Imports
#
from . RM_Socket import RM_Socket
from . RM_NodeSocketIntInterface import RM_NodeSocketIntInterface
from . util import update_func
from .. import rfb


# socket types (need this just for the ui_open)
class RM_NodeSocketInt(NodeSocketInt, RM_Socket):
    """RenderMan input/output int socket."""
    bl_idname = 'RendermanNodeSocketInt'
    bl_label = 'RenderMan Int Socket'

    default_value = IntProperty(update=update_func)
    renderman_type = StringProperty(default='int')

    def draw_color(self, context, node):
        return rfb.reg.get('INT')

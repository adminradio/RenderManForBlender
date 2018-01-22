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
from bpy.props import BoolProperty

#
# RenderMan for Blender Imports
#
from . RM_SocketMixin import RM_SocketMixin
from .. import rfb


_group_nodes = [
    'ShaderNodeGroup',
    'NodeGroupInput',
    'NodeGroupOutput'
]


# socket name corresponds to the param on the node
class RM_Socket:
    ui_open = BoolProperty(name='UI Open', default=True)

    def get_pretty_name(self, node):
        if node.bl_idname in _group_nodes:
            return self.name
        else:
            return self.identifier

    def get_value(self, node):
        if (node.bl_idname in _group_nodes or not hasattr(node, self.name)):
            return self.default_value
        else:
            return getattr(node, self.name)

    def draw_color(self, context, node):
        return rfb.reg.get('BXDF')

    def draw_value(self, context, layout, node):
        layout.prop(node, self.identifier)

    def draw(self, context, layout, node, text):
        if self.is_linked or \
                self.is_output or \
                self.hide_value or not \
                hasattr(self, 'default_value'):

            layout.label(self.get_pretty_name(node))

        elif node.bl_idname in _group_nodes or \
                node.bl_idname == "PxrOSLPatternNode":
            layout.prop(
                self, 'default_value',
                text=self.get_pretty_name(node),
                slider=True
            )
        else:
            layout.prop(
                node, self.name,
                text=self.get_pretty_name(node),
                slider=True
            )

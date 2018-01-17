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
# Blender Imports
#
from bpy.types import Panel

#
# RenderMan for Blender Imports
#
from . RfB_PT_MIXIN_ShaderTypePolling import RfB_PT_MIXIN_ShaderTypePolling
from .. nodes import draw_nodes_properties_ui


class RfB_PT_MATERIAL_ShaderLight(RfB_PT_MIXIN_ShaderTypePolling, Panel):
    bl_context = "material"
    bl_label = "Light Emission"
    shader_type = 'Light'

    def draw(self, context):
        if context.material.node_tree:
            nt = context.material.node_tree
            draw_nodes_properties_ui(
                self.layout, context, nt, input_name=self.shader_type)

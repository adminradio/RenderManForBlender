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
# blender imports
#
import bpy

#
# RenderMan for Blender
#
from .. nds.util import is_renderman


class RfB_HT_NODE_SmartControl(bpy.types.Header):
    bl_idname = 'rfb_ht_node_smart_control'
    bl_space_type = "NODE_EDITOR"

    def draw(self, context):
        if context.scene.render.engine != "PRMAN_RENDER":
            return
        layout = self.layout

        row = layout.row(align=True)

        if (hasattr(context.space_data, 'id')
                and type(context.space_data.id) == bpy.types.Material
                and not is_renderman(context.space_data.id)):
            row.operator(
                'rfb.node_add_nodetree',
                text="Convert to RenderMan"
            ).idtype = "node_editor"

        row.operator('rfb.material_new_bxdf')

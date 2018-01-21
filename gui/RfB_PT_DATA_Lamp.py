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
from .. import engine


class RfB_PT_DATA_Lamp(RfB_PT_MIXIN_ShaderTypePolling, Panel):
    bl_context = "data"
    bl_label = "Lamp"
    shader_type = 'light'

    def draw(self, context):
        layout = self.layout

        lamp = context.lamp
        ipr_running = True if engine.ipr else False  # != None  # FIXME: E711
        if not lamp.renderman.use_renderman_node:
            layout.prop(lamp, "type", expand=True)
            layout.operator('rfb.node_add_nodetree').idtype = 'lamp'
            layout.operator('rfb.node_cycles_convertall')
            return
        else:
            if ipr_running:
                layout.label(
                    "Note: Some items cannot be edited while IPR running.")
            row = layout.row()
            row.enabled = not ipr_running
            row.prop(lamp.renderman, "renderman_type", expand=True)
            if lamp.renderman.renderman_type == 'FILTER':
                row = layout.row()
                row.enabled = not ipr_running
                row.prop(lamp.renderman, "filter_type", expand=True)
            if lamp.renderman.renderman_type == "AREA":
                row = layout.row()
                row.enabled = not ipr_running
                row.prop(lamp.renderman, "area_shape", expand=True)
                row = layout.row()
                if lamp.renderman.area_shape == "rect":
                    row.prop(lamp, 'size', text="Size X")
                    row.prop(lamp, 'size_y')
                else:
                    row.prop(lamp, 'size', text="Diameter")
            # layout.prop(lamp.renderman, "shadingrate")
        # layout.prop_search(lamp.renderman, "nodetree", bpy.data, "node_groups")
        row = layout.row()
        row.enabled = not ipr_running
        row.prop(lamp.renderman, 'illuminates_by_default')

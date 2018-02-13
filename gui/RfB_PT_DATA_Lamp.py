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
# RenderManForBlender Imports
#
from . RfB_PT_MIXIN_ShaderTypePolling import RfB_PT_MIXIN_ShaderTypePolling
from . import icons
from .. import engine


class RfB_PT_DATA_Lamp(RfB_PT_MIXIN_ShaderTypePolling, Panel):
    bl_context = "data"
    bl_label = "Lamp"
    shader_type = 'light'

    def draw(self, context):
        layout = self.layout

        __l = context.lamp
        __r = __l.renderman
        __t = __r.renderman_type

        ipr = engine.ipr is not None
        if not __r.use_renderman_node:
            layout.prop(__l, "type", expand=True)
            layout.operator('rfb.node_add_nodetree').idtype = 'lamp'
            layout.operator('rfb.node_cycles_convertall')
            return
        else:
            if ipr:
                txt = "Some items cannot be edited while IPR running."
                layout.label(txt, icon='ERROR')
            row = layout.row(align=True)
            row.enabled = not ipr
            iid = icons.toggle('light', __r.illuminates_by_default)
            row.prop(__r, 'illuminates_by_default', text="", icon_value=iid)
            row.prop(__r, "renderman_type", expand=True)

            if __t == 'FILTER':
                row = layout.row()
                row.enabled = not ipr
                row.prop(__r, "filter_type", expand=True)

            if __t == "AREA":
                row = layout.row(align=True)
                row.enabled = not ipr
                row.prop(__r, "area_shape", expand=True)
                row = layout.row(align=True)
                if __r.area_shape == "rect":
                    row.prop(__l, 'size', text="Size X")
                    row.prop(__l, 'size_y')
                else:
                    row.prop(__l, 'size', text="Diameter")
            # layout.prop(__lrenderman, "shadingrate")
        # layout.prop_search(__lrenderman, "nodetree", bpy.data, "node_groups")

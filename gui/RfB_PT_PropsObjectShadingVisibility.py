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
import bpy
from bpy.types import Panel

#
# RenderMan for Blender Imports
#
# from . import icons

from . RfB_PT_Collection import RfB_PT_Collection


class RfB_PT_PropsObjectShadingVisibility(RfB_PT_Collection, Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_label = "Shading and Visibility"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (context.object and rd.engine in {'PRMAN_RENDER'})

    def draw_item(self, layout, context, item):
        ob = context.object
        rm = bpy.data.objects[ob.name].renderman
        ll = rm.light_linking
        index = rm.light_linking_index

        col = layout.column()
        col.prop(item, "group")
        col.prop(item, "mode")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        rm = ob.renderman

        col = layout.column()
        row = col.row()
        row.prop(rm, "visibility_camera", text="Camera")
        row.prop(rm, "visibility_trace_indirect", text="Indirect")
        row = col.row()
        row.prop(rm, "visibility_trace_transmission", text="Transmission")
        row.prop(rm, "matte")
        row = col.row()
        row.prop(rm, "holdout")

        col.separator()

        icon = 'CHECKBOX_HLT' if rm.shading_override else 'CHECKBOX_DEHLT'

        cl = col.box()
        row = cl.row()
        row.prop(rm, 'shading_override', icon=icon, emboss=False)

        if rm.shading_override:
            colgroup = cl.column()
            colgroup.enabled = rm.shading_override
            row = colgroup.row()
            row.prop(rm, "watertight")
            row = colgroup.row()
            row.prop(rm, "shadingrate")
            row = colgroup.row()
            row.prop(rm, "geometric_approx_motion")
            row = colgroup.row()
            row.prop(rm, "geometric_approx_focus")

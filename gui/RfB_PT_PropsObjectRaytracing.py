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
# from . import icons

from . RfB_PT_Collection import RfB_PT_Collection


class RfB_PT_PropsObjectRaytracing(RfB_PT_Collection, Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_label = "Ray Tracing"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (context.object and rd.engine in {'PRMAN_RENDER'})

    def draw_item(self, layout, context, item):
        col = layout.column()
        col.prop(item, "group")
        col.prop(item, "mode")

    def draw(self, context):
        layout = self.layout
        ob = context.object
        rm = ob.renderman

        col = layout.column()
        row = col.row(align=True)
        row.prop(
            rm, "raytrace_intersectpriority", text="Intersection Priority")
        row.prop(rm, "raytrace_ior")

        col.separator()

        icon = 'CHECKBOX_HLT' if rm.raytrace_override else 'CHECKBOX_DEHLT'
        cl = col.box()
        cl.prop(rm,
                "raytrace_override",
                text="Override Default Ray Tracing",
                icon=icon, emboss=False)

        if rm.raytrace_override:
            col = cl.column()
            col.active = rm.raytrace_override
            row = col.row()
            row.prop(rm, "raytrace_pixel_variance")
            row = col.row()
            row.prop(rm, "raytrace_maxdiffusedepth", text="Max Diffuse Depth")
            row = col.row()
            row.prop(rm, "raytrace_maxspeculardepth", text="Max Specular Depth")
            row = col.row()
            row.prop(rm, "raytrace_tracedisplacements", text="Trace Displacements")
            row = col.row()
            row.prop(rm, "raytrace_autobias", text="Ray Origin Auto Bias")
            row = col.row()
            row.prop(rm, "raytrace_bias", text="Ray Origin Bias Amount")
            row.active = not rm.raytrace_autobias
            row = col.row()
            row.prop(rm, "raytrace_samplemotion", text="Sample Motion Blur")
            row = col.row()
            row.prop(rm, "raytrace_decimationrate", text="Decimation Rate")

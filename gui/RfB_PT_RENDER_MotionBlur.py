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
# from . import icons

from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_RENDER_MotionBlur(RfB_PT_MIXIN_Panel, Panel):
    # class RENDER_PT_renderman_motion_blur(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "Motion Blur"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        rm = context.scene.renderman
        layout = self.layout

        cl = layout.box()
        icon = 'CHECKBOX_HLT' if rm.motion_blur else 'CHECKBOX_DEHLT'
        cl.prop(rm, "motion_blur", icon=icon, emboss=False)

        if rm.motion_blur:
            sub = cl.row()
            sub.enabled = rm.motion_blur
            sub.prop(rm, "motion_segments")

            row = cl.row()
            row.enabled = rm.motion_blur
            row.prop(rm, "sample_motion_blur")

            row = cl.row()
            row.enabled = rm.motion_blur
            row.prop(rm, "shutter_timing")

            row = cl.row()
            row.enabled = rm.motion_blur
            row.prop(rm, "shutter_angle")

            row = cl.row()
            row.enabled = rm.motion_blur
            row.prop(rm, "shutter_efficiency_open")
            row.prop(rm, "shutter_efficiency_close")

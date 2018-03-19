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
# blender imports
#
import bpy

#
# RenderMan for Blender imports
#
from .. import engine
from . icons import iconid
from . icons import toggle


class RfB_HT_INFO_SmartControl(bpy.types.Header):
    bl_idname = 'rfb_ht_info_smart_control'
    bl_space_type = "INFO"

    def draw(self, context):
        if context.scene.render.engine != "PRMAN_RENDER":
            return

        rmn = context.scene.renderman

        layout = self.layout
        layout.enabled = True if bpy.context.scene.camera else False

        row = layout.row(align=True)
        row.scale_x = 1.25
        iid = iconid("render")
        row.operator("render.render", text="", icon_value=iid)

        iid = iconid("batch_render")
        opr = "render.render"
        row.operator(opr, text="", icon_value=iid).animation = True

        iid = iconid("stop_ipr") if engine.ipr else iconid("start_ipr")
        opr = "rfb.tool_ipr"
        row.operator(opr, text="", icon_value=iid)

        row = layout.row(align=True)
        prp = "enable_external_rendering"
        iid = toggle('spool', rmn.enable_external_rendering)
        row.prop(rmn, prp, icon_only=True, icon_value=iid)
        if rmn.enable_external_rendering:
            prp = "external_animation"
            iid = toggle("animation", rmn.external_animation)
            row.prop(rmn, prp, icon_only=True, icon_value=iid)
            row = layout.row(align=True)
            row.scale_x = 1.25
            iid = iconid("render_spool")
            opr = "rfb.file_spool_render"
            row.operator(opr, text="", icon_value=iid)

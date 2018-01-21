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
from . import icons
from .. import engine


class RfB_HT_INFO_SmartControl(bpy.types.Header):
    bl_idname = 'rfb_ht_info_smart_control'
    bl_space_type = 'INFO'

    def draw(self, context):
        if context.scene.render.engine != 'PRMAN_RENDER':
            return
        layout = self.layout

        row = layout.row(align=True)
        opr = 'render.render'
        iid = icons.iconid('render')
        row.operator(opr, text="Render", icon_value=iid)

        if context.scene.renderman.enable_external_rendering:
            opr = 'rfb.file_spool_render'
            txt = "Spool"
            iid = icons.iconid('render_spool')
            row.operator(opr, text=txt, icon_value=iid)
        if engine.ipr:
            opr = 'rfb.tool_ipr'
            txt = "IPR"
            iid = icons.iconid('stop_ipr')
            row.operator(opr, text=txt, icon_value=iid)
        else:
            opr = 'rfb.tool_ipr'
            txt = "IPR"
            iid = icons.iconid('start_ipr')
            row.operator(opr, text=txt, icon_value=iid)

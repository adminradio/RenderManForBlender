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
# Blender imports
#
import bpy

#
# RenderMan for Blender
#
from . import icons


class RfB_MT_SCENE_LightsHemi(bpy.types.Menu):
    bl_idname = "rfb_mt_scene_lightshemi"
    bl_label = "EnvLight List"

    icn = icons.iconid('envlight')

    def draw(self, context):
        layout = self.layout
        # col = layout.column(align=True)

        lamps = [obj for obj in bpy.context.scene.objects if obj.type == "LAMP"]

        if len(lamps):
            for lamp in lamps:
                if lamp.data.type == 'HEMI':
                    name = lamp.name
                    op = layout.operator(
                        "rfb.object_select_light", text=name, icon_value=self.icn)
                    op.light_name = name

        else:
            layout.label("No EnvLight in the Scene")

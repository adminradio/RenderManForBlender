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

import bpy
from .. import icons
# from .. import ops
from .. ops import RfB_OT_SelectLight


class RfB_MT_AreaLights(bpy.types.Menu):
    """Create a menu of all area lights found in current scene."""
    bl_idname = "rfb.area_lights_menu"
    bl_label = "Area Light List"

    def draw(self, context):
        layout = self.layout
        iid = icons.iconid('arealight')

        lamps = [obj for obj in bpy.context.scene.objects if obj.type == "LAMP"]
        if lamps:
            for lamp in lamps:
                if lamp.data.type == 'AREA':
                    name = lamp.name
                    op = layout.operator(
                        "object.selectlight", text=name, icon_value=iid)
                    op.light_name = name
        else:
            layout.label("No AreaLight in the Scene.")

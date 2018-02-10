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
# Python Imports
#

#
# Blender Imports
#
import bpy

#
# RenderManForBlender Imports
#
from . import icons


class RfB_MT_MIXIN_Lamps(bpy.types.Menu):
    bl_idname = "RFB_MT_MIXIN_LAMPS"
    bl_label = "SELECT LAMP"
    typ = "LAMP"
    eid = icons.iconid('empty')
    opr = "rfb.object_select_light"

    dtyp = "DATA"         # Override: data type
    tmpl = "LAMP LIGHT"   # Override: template
    icon = 'pointlight'   # Override: name for icon id

    def __init__(self):
        self.iid = icons.iconid(self.icon)

    def draw(self, context):
        mnu = self.layout
        obs = bpy.context.scene.objects

        items = [
            obj for obj in obs
            if obj.type == self.typ
            and obj.data.type == self.dtyp
        ]

        if items:
            sobj = bpy.context.selected_objects
            items.sort(key=lambda x: x.name)
            sobj = bpy.context.selected_objects
            for item in items:
                iid = self.iid if item in sobj else self.eid
                txt = item.name
                sop = mnu.operator(self.opr, text=txt, icon_value=iid)
                sop.light_name = txt
        else:
            mnu.label("No {} in Scene!".format(self.tmpl), icon_value=self.iid)

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

#
# RenderMan for Blender Imports
#
from . import icons


class RfB_UL_LightLinkingObjects(bpy.types.UIList):
    iid_on = icons.iconid('ll_on')
    iid_off = icons.iconid('ll_off')
    iid_default = icons.iconid('ll_default')
    iid_unlinked = icons.iconid('ll_unlinked')

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        rm = context.scene.renderman

        light_type = rm.ll_light_type
        lg = bpy.data.lamps if light_type == "light" else rm.light_groups
        ll_prefix = "lg_%s>%s>obj_%s>%s" % (
            light_type, lg[rm.ll_light_index].name, rm.ll_object_type, item.name)

        # default to symbol: 'unlinked'
        iid = self.iid_unlinked

        if ll_prefix in rm.ll.keys():
            ll = rm.ll[ll_prefix]

            # override 'unlinked' with 'default'
            if ll.illuminate == 'DEFAULT':
                iid = self.iid_default

            # or override 'unlinked' with 'on'
            elif ll.illuminate == 'ON':
                iid = self.iid_on

            # guess what? override with 'off'
            else:
                iid = self.iid_off

        layout.alignment = 'LEFT'
        layout.label(item.name, icon_value=iid)

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
# RenderManForBlender Imports
#
from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


#
# TODO:   Loading a file should also be possible. Currently you can
#         only assign internel text data blocks.
# DATE:   2018-01-17
# AUTHOR: Timm Wimmers
# STATUS: -unassigned-
#
class RfB_PT_MIXIN_RIBInjection(RfB_PT_MIXIN_Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "RIB Box"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (rd.engine in {'PRMAN_RENDER'})

    def draw_rib_boxes(self, layout, rib_box_names, item):
        rm = item.renderman
        for rib_box in rib_box_names:
            row = layout.row()
            row.prop_search(rm, rib_box, bpy.data, "texts")
            if getattr(item.renderman, rib_box) != '':
                text_name = getattr(item.renderman, rib_box)
                rib_box_string = bpy.data.texts.get(text_name)
                for line in rib_box_string.lines:
                    row = layout.row()
                    row.label(text=line.body)

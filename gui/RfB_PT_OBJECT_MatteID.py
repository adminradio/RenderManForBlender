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


class RfB_PT_OBJECT_MatteID(RfB_PT_MIXIN_Panel, Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_label = "Matte ID"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (context.object and rd.engine in {'PRMAN_RENDER'})

    def draw(self, context):
        layout = self.layout.column(align=True)
        ob = context.object
        rm = ob.renderman

        row = layout.row(align=True)
        row.prop(rm, 'MatteID0', text='')
        row.prop(rm, 'MatteID1', text='')
        row.prop(rm, 'MatteID2', text='')
        row.prop(rm, 'MatteID3', text='')

        row = layout.row(align=True)
        row.prop(rm, 'MatteID4', text='')
        row.prop(rm, 'MatteID5', text='')
        row.prop(rm, 'MatteID6', text='')
        row.prop(rm, 'MatteID7', text='')

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
from . RfB_PT_MIXIN_Collection import RfB_PT_MIXIN_Collection


class RfB_PT_DATA_LightFilters(RfB_PT_MIXIN_Collection, Panel):
    bl_label = "Light Filters"
    bl_context = 'data'

    def draw_item(self, layout, context, item):
        layout.prop(item, 'filter_name')

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return (
            rd.engine == 'PRMAN_RENDER' and
            hasattr(context, "lamp") and
            context.lamp is not None and
            hasattr(context.lamp, 'renderman')and
            context.lamp.renderman.renderman_type != 'FILTER'
        )

    def draw(self, context):
        layout = self.layout
        lamp = context.lamp

        self._draw_collection(
            context, layout, lamp.renderman, "-=Light Filters=-",
            "rfb.collection_toggle_path", "lamp", "light_filters",
            "light_filters_index"
        )

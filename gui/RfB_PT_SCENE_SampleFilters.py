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

# <pep8 compliant>

#
# Blender Imports
#
from bpy.types import Panel

#
# RenderMan for Blender Imports
#
from . RfB_PT_MIXIN_Collection import RfB_PT_MIXIN_Collection
from . utils import draw_props


class RfB_PT_SCENE_SampleFilters(RfB_PT_MIXIN_Collection, Panel):
    bl_idname = "rfb_pt_scene_samplefilters"
    bl_label = "Sample Filters"
    bl_context = 'scene'

    def draw_item(self, layout, context, item):
        layout.prop(item, 'filter_type')
        layout.separator()
        filter_node = item.get_filter_node()
        draw_props(filter_node, filter_node.prop_names, layout)

    @classmethod
    def poll(cls, context):
        rd = context.scene.render
        return rd.engine == 'PRMAN_RENDER'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        self._draw_collection(context, layout, rm, "",
                              "rfb.collection_toggle_path", "scene",
                              "sample_filters", "sample_filters_index")

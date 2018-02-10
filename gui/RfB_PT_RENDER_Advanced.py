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


class RfB_PT_RENDER_Advanced(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "Advanced"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        layout.separator()

        col = layout.column()
        col.prop(rm, "shadingrate")
        col.prop(rm, "dicing_strategy")
        row = col.row()
        row.enabled = rm.dicing_strategy == "worlddistance"
        row.prop(rm, "worlddistancelength")
        col.prop(rm, "instanceworlddistancelength")

        layout.separator()

        col = layout.column()
        col.prop(rm, "texture_cache_size")
        col.prop(rm, "geo_cache_size")
        col.prop(rm, "opacity_cache_size")

        layout.separator()
        col = layout.column()
        row = col.row()
        row.label("Pixel Filter:")
        row.prop(rm, "pixelfilter", text="")
        row = col.row(align=True)
        row.prop(rm, "pixelfilter_x", text="Size X")
        row.prop(rm, "pixelfilter_y", text="Size Y")

        layout.separator()
        col = layout.column()
        col.prop(rm, "dark_falloff")

        layout.separator()
        col = layout.column()
        col.prop(rm, "bucket_shape")
        if rm.bucket_shape == 'SPIRAL':
            row = col.row(align=True)
            row.prop(rm, "bucket_spiral_x", text="X")
            row.prop(rm, "bucket_spiral_y", text="Y")

        layout.separator()
        col = layout.column()
        row = col.row()
        row.prop(rm, "use_statistics", text="Output stats")
        row.operator('rfb.file_view_stats')
        row = col.row()
        row.operator('rfb.file_open_last_rib')
        row.prop(rm, "editor_override")
        row = layout.row()
        row.label(text="RIB Format:")
        row.label(text="RIB Compression")
        row = layout.row()
        row.prop(rm, "rib_format", text="")
        row.prop(rm, "rib_compression", text="")

        layout.separator()
        layout.prop(rm, "always_generate_textures")
        layout.prop(rm, "lazy_rib_gen")
        layout.prop(rm, "threads")

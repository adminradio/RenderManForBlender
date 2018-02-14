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
from . utils import split12

from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_RENDER_Advanced(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "Advanced"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        rm = scene.renderman

        lay = layout.column()

        lco, rco = split12(lay, align=True)

        lco.label("Micropolygon Length:")
        rco.prop(rm, "shadingrate", text="")

        lco.separator()
        rco.separator()

        # _l_ = lco.column(align=True)
        # _r_ = rco.column(align=True)

        lco.label("Dicing Strategy:")
        lco.label("World Dist. Length:")
        lco.label("Instance World Dist. Length:")

        rco.prop(rm, "dicing_strategy", text="")
        row = rco.row(align=True)
        row.enabled = rm.dicing_strategy == "worlddistance"
        row.prop(rm, "worlddistancelength", text="")
        rco.prop(rm, "instanceworlddistancelength", text="")

        lco.separator()
        rco.separator()

        lco.label("Cache Sizes (MB):")
        lco.label("")
        lco.label("")
        col = rco.column(align=True)
        col.prop(rm, "texture_cache_size", text="Texture")
        col.prop(rm, "geo_cache_size", text="Geometry")
        col.prop(rm, "opacity_cache_size", text="Opacity")

        lco.separator()
        rco.separator()

        lco.label("Pixel Filter:")
        lco.label("")
        rco.prop(rm, "pixelfilter", text="")
        row = rco.row(align=True)
        row.prop(rm, "pixelfilter_x", text="Size X")
        row.prop(rm, "pixelfilter_y", text="Size Y")

        lco.separator()
        rco.separator()

        lco.label("Dark Falloff:")
        rco.prop(rm, "dark_falloff", text="")

        lco.separator()
        rco.separator()

        lco.label("Bucket Order:")
        rco.prop(rm, "bucket_shape", text="")
        if rm.bucket_shape == 'SPIRAL':
            lco.label("")
            row = rco.row(align=True)
            row.prop(rm, "bucket_spiral_x", text="X")
            row.prop(rm, "bucket_spiral_y", text="Y")

        lco.separator()
        rco.separator()

        lco.label("Texteditor:")
        rco.prop(rm, "editor_override", text="")

        lco.separator()
        rco.separator()

        lco.label(text="RIB Format:")
        rco.prop(rm, "rib_format", text="")

        lco.separator()
        rco.separator()

        lco.label(text="RIB Compression")
        rco.prop(rm, "rib_compression", text="")

        lco.separator()
        rco.separator()

        lco.label("")
        rco.operator('rfb.file_open_last_rib')

        lco.separator()
        rco.separator()

        lco.label("Rendering Threads:")
        rco.prop(rm, "threads", text="")

        lco.separator()
        rco.separator()

        lco.label("")
        row = rco.row(align=True)
        row.prop(rm, "use_statistics", text="", icon='FCURVE')
        row.operator('rfb.file_view_stats')

        lco.separator()
        rco.separator()

        rco.prop(rm, "always_generate_textures")
        rco.prop(rm, "lazy_rib_gen")

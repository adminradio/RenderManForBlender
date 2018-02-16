# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2015 - 2018 Pixar
#
# Pe__rission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to pe__rit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this pe__rission notice shall be included in
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


class RfB_PT_RENDER_PreviewSampling(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "IPR and Preview Sampling"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        __s = context.scene
        __r = __s.renderman

        lco, rco = split12(layout)
        lco.label("Preview Pixel Variance:")
        rco.prop(__r, "preview_pixel_variance", text="")

        lco.label("Samples:")
        row = rco.row(align=True)
        row.prop(__r, "preview_min_samples", text="Min.")
        row.prop(__r, "preview_max_samples", text="Max.")

        lco.label("Depth:")
        row = rco.row(align=True)
        row.prop(__r, "preview_max_specular_depth", text="Specular")
        row.prop(__r, "preview_max_diffuse_depth", text="Diffuse")

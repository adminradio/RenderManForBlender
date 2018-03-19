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
# import bpy
from bpy.types import Panel

#
# RenderManForBlender Imports
#
from . utils import split12

from . RfB_PT_MIXIN_Panel import RfB_PT_MIXIN_Panel


class RfB_PT_LAYER_LayerOptions(RfB_PT_MIXIN_Panel, Panel):
    bl_label = "Layer"
    bl_context = "render_layer"

    def draw(self, context):
        lay = self.layout
        scn = context.scene
        rnd = context.scene.render
        rmn = context.scene.renderman

        lco, rco = split12(lay)
        lco.label("Scene:")
        rco.prop(scn, "layers", text="")

        _l_ = None
        for l in rmn.render_layers:
            if l.render_layer == rnd.layers.active.name:
                _l_ = l
                break
        if _l_ is None:
            return
            # lay.operator('renderman.add_pass_list')
        else:
            lco, rco = split12(lay)
            #
            # TODO:   Implement Multicamera Export
            # DATE:   2018-02-27
            # AUTHOR: Timm Wimmers
            # STATUS: -unassigned-
            #
            # cutting this for now until we can export multiple cameras
            # lco.label("Cameras:")
            # rco.prop_search(_l_, 'camera', bpy.data, 'cameras', text="")
            #
            lco.label("Light Group:")
            lco.label("Object Group:")
            rco.prop_search(_l_, 'light_group',
                            rmn, 'light_groups', icon='DOT', text="")
            rco.prop_search(_l_, 'object_group',
                            rmn, 'object_groups', icon='DOT', text="")
            rco.prop(_l_, "denoise_aov")

            rco.prop(_l_, 'export_multilayer')
            if _l_.export_multilayer:
                rco.prop(_l_, 'use_deep')
                lay.prop(_l_, "exr_format_options", text="Bit Depth")
                lay.prop(_l_, "exr_compression", text="Compression")
                lay.prop(_l_, "exr_storage", text="Storage Mode")
